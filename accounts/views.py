import json
import os
import datetime
import stripe
import secrets
import logging
import traceback
from os.path import exists

from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import logout, get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import Account
from .forms import EditProfileForm, UserMembershipForm, SelfLeaderCreationForm, LeaderUniqueTokenForm, \
    SelfTeacherCreationForm, TeacherUniqueTokenForm
from datetime import timedelta
from settings.models import Membership
from subscription.models import Subscription
from settings.models import Country, StripeGateway
from core.decorators import superuser_required
# WhatsApp Twilio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# PDF Generation
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfFileReader, PdfFileWriter
# PDF to Image Conversion
from pdf2image import convert_from_path

User = get_user_model()

# For Error Logging
logger = logging.getLogger(__name__)

# Stripe Payment for New Leader Registration
stripe.api_key = StripeGateway.secret_key


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, _('You are now logged in.'))
            return redirect('dashboard')
        else:
            messages.error(request, _('Invalid Login Credentials.'))
            return redirect('login')

    return render(request, 'front/members/login.html')


@login_required(login_url='login')
def LeaderRegistration(request):
    all_countries = Country.objects.all()
    context = {
        'all_countries': all_countries,
    }
    return render(request, 'front/members/registration/leader-registration.html', context)


def charge(request):
    if request.method != 'POST':
        return redirect(reverse('leaders-registration'))

    data = extract_lut_form_data(request)

    # Check if Stripe Transaction was successful
    if not create_lut_stripe_transaction(data, request):
        return redirect('leaders-registration')

    # Creating token for leader registration
    transaction_token = store_lut_transaction(data, request.user)

    # Send Confirmation Email
    if not send_lut_confirmation_email(data, transaction_token):
        messages.error(request, 'Error sending the email.')
        return redirect(reverse('success', args=[transaction_token]))

    # Send WhatsApp Notification
    if not send_lut_whatsapp_notification(data, transaction_token):
        messages.error(request, 'Error sending the WhatsApp notification')
        return redirect(reverse('success', args=[transaction_token]))

    return redirect(reverse('success', args=[transaction_token]))


def extract_lut_form_data(request):
    form_fields = [
        'fullname', 'email', 'address', 'city',
        'state', 'country', 'postalcode', 'quantity', 'contact'  # <- Add 'contact' here
    ]
    return {field: request.POST.get(field, '') for field in form_fields}


# Stripe Transaction
def create_lut_stripe_transaction(data, request):
    try:
        customer = stripe.Customer.create(
            name=data['fullname'],
            email=data['email'],
            address={
                'city': data['city'],
                'country': data['country'],
                'line1': data['address'],
                'postal_code': data['postalcode'],
                'state': data['state'],
            },
            source=request.POST.get('stripeToken'),
        )
        stripe.Charge.create(
            customer=customer,
            amount=int(data['quantity']) * 1000,
            currency='usd',
            description='New Leader Registration',
        )
        return True
    except stripe.error.StripeError as e:
        logging.error(f"Stripe Error: {e}")
        messages.error(request, f"Stripe Error: {e}")
        return False


def store_lut_transaction(data, current_user):
    token = secrets.token_urlsafe(16)
    lut_transaction = create_lut_transaction(data, current_user, token)
    lut_transaction.save()
    return token


def create_lut_transaction(data, current_user, token):
    transaction = LeaderUniqueToken(
        user=current_user,
        amount=int(data['quantity']) * 10,
        quantity=data['quantity'],
        count=data['quantity'],
        token=token,
    )
    return transaction

# Confirmation Email
def send_lut_confirmation_email(data, token):
    try:
        # Subject and email receivers
        mail_subject = f'{data["fullname"]} paid for {data["quantity"]} Leaders.'
        from_email = f'Laughter Yoga International <{settings.DEFAULT_FROM_EMAIL}>'
        to_email = (data['email'], 'Laughter Yoga International <help@laughteryoga.org>')
        # Message content
        message_content = {
            'fullname': data['fullname'],
            'email': data['email'],
            'address': data['address'],
            'city': data['city'],
            'state': data['state'],
            'country': data['country'],
            'postalcode': data['postalcode'],
            'amount': int(data['quantity']) * 10, # Use get to avoid KeyError
            'quantity': data['quantity'],
            'token': token, # Use get to avoid KeyError
        }
        # Determine the email template based on the course
        email_template = 'front/email/leader-registration-email.html'
        html_content = render_to_string(email_template, message_content)
        # Send the email
        send_mail(mail_subject, None, from_email, to_email, html_message=html_content)
        return True
    except BadHeaderError:
        return False
    except Exception as e:
        # Ideally, log the exception for debugging
        logging.error(f"Error sending email: {e} \n{traceback.format_exc()}")
        return False

# Confirmation Whatsapp Notification
def send_lut_whatsapp_notification(data, token):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        contact = data.get('contact', '').strip()  # Ensure contact exists and trim any whitespace
        if not contact:
            logging.error("Contact number missing or not provided.")
            return False

        country_name = data.get('country')  # This gets the selected country's name from the dropdown

        # 👉🏻 Fetch the country code from the Country model
        try:
            country_obj = Country.objects.get(name=country_name)
            country_code = country_obj.country_code
        except Country.DoesNotExist:
            logging.error(f"No country found in database with name: {country_name}")
            return False

        to_whatsapp_number = f'whatsapp:+{country_code}{contact}'
        # to_whatsapp_number = f'whatsapp:+91{contact}'  # adjust if international

        contentVariables = {
            '1': str(data['quantity']),
            '2': str(token),
            '3': str(data['fullname']),
        }

        client.messages.create(
            content_sid='HX7b3b0757d3feb52cdf0f4e37c272f6c0',
            content_variables=json.dumps(contentVariables),
            from_='MG0485ae03bc7fb111cb65a6bd21b10938',
            to=to_whatsapp_number
        )
        return True

    except KeyError as ke:
        logging.error(f"KeyError while processing data for WhatsApp notification: {ke}\n{traceback.format_exc()}")
        return False
    except TwilioRestException as tre:
        logging.error(f"Twilio Error while sending WhatsApp notification: {tre}\n{traceback.format_exc()}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error sending WhatsApp notification: {e}\n{traceback.format_exc()}")
        return False

@login_required(login_url='login')
def successMsg(request, args):
    user_token = get_object_or_404(LeaderUniqueToken, token=args)
    context = {
        'user_token': user_token,
    }

    return render(request, 'front/members/registration/success.html', context)


def selfLeaderCreation(request, args):
    user_token = get_object_or_404(LeaderUniqueToken, token=args)
    if user_token.count != 0:
        if request.method == 'POST':
            form = SelfLeaderCreationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.user_type = 'Certified Leader'
                user.membership = 'active'
                user.token = user_token.token
                user.save()

                # Create a user membership
                user_membership = UserMembershipForm()
                user_membership.user = user
                user_membership.membership = Membership.objects.get(membership_slug='membership-6-months')
                user_membership.start_date = timezone.now()
                user_membership.expiry_date = user_membership.start_date + timedelta(days=user_membership.membership.membership_duration)
                user_membership.token = user_token.token
                user_membership = Subscription.objects.create(
                    user=user_membership.user,
                    membership=user_membership.membership,
                    start_date=user_membership.start_date,
                    expiry_date=user_membership.expiry_date,
                    token=user_membership.token,
                    active=True
                )
                user_membership.save()

                # Reduce Token Count
                leader_token = LeaderUniqueToken.objects.get(token=user_token)
                leader_token.count = user_token.count - 1
                leader_token.save()

                # User Auto Login
                auth.login(request, user)
                messages.success(request, 'Successfully logged in. Now please update your profile page.')
                return redirect('edit-profile')
        else:
            form = SelfLeaderCreationForm()
    else:
        messages.warning(request, '- You have exhausted registration limit.')
        return redirect('login')

    context = {
        'form': form,
    }

    return render(request, 'front/members/leader-register.html', context)


@login_required(login_url='login')
def teacherRegistration(request):
    all_countries = Country.objects.all()
    context = {
        'all_countries': all_countries,
    }
    return render(request, 'front/members/registration/teacher-registration.html', context)


def teacherCharge(request):
    if request.method != 'POST':
        return redirect(reverse('teacher-registration'))

    data = extract_tut_form_data(request)

    # Check if Stripe Transaction was successful
    if not create_tut_stripe_transaction(data, request):
        return redirect('teacher-registration')

    # Creating token for leader registration
    transaction_token = store_tut_transaction(data, request.user)

    # Send Confirmation Email
    if not send_tut_confirmation_email(data, transaction_token):
        messages.error(request, 'Error sending the email.')
        return redirect(reverse('teacher-success', args=[transaction_token]))

    # Send WhatsApp Notification
    if not send_tut_whatsapp_notification(data, transaction_token):
        messages.error(request, 'Error sending the WhatsApp notification')
        return redirect(reverse('teacher-success', args=[transaction_token]))

    return redirect(reverse('teacher-success', args=[transaction_token]))


def extract_tut_form_data(request):
    form_fields = [
        'fullname', 'email', 'address', 'city',
        'state', 'country', 'postalcode', 'contact', 'quantity', 'price'
    ]
    return {field: request.POST.get(field, '') for field in form_fields}


# Stripe Transaction
def create_tut_stripe_transaction(data, request):
    try:
        customer = stripe.Customer.create(
            name=data['fullname'],
            email=data['email'],
            address={
                'city': data['city'],
                'country': data['country'],
                'line1': data['address'],
                'postal_code': data['postalcode'],
                'state': data['state'],
            },
            source=request.POST.get('stripeToken'),
        )
        stripe.Charge.create(
            customer=customer,
            amount=(int(data['quantity']) * int(data['price'])) * 100,
            currency='usd',
            description='New Teacher Registration',
        )
        return True
    except stripe.error.StripeError as e:
        logging.error(f"Stripe Error: {e}")
        messages.error(request, f"Stripe Error: {e}")
        return False


def store_tut_transaction(data, current_user):
    token = secrets.token_urlsafe(16)
    tut_transaction = create_tut_transaction(data, current_user, token)
    tut_transaction.save()
    return token


def create_tut_transaction(data, current_user, token):
    transaction = TeacherUniqueToken(
        user=current_user,
        amount=int(data['quantity']) * int(data['price']),
        quantity=data['quantity'],
        count=data['quantity'],
        token=token,
    )
    return transaction


# Confirmation Email
def send_tut_confirmation_email(data, token):
    try:
        # Subject and email receivers
        mail_subject = f'{data["fullname"]} paid for {data["quantity"]} Teachers.'
        from_email = f'Laughter Yoga International <{settings.DEFAULT_FROM_EMAIL}>'
        to_email = (data['email'], 'Laughter Yoga International <help@laughteryoga.org>')
        # Message content
        message_content = {
            'fullname': data['fullname'],
            'email': data['email'],
            'address': data['address'],
            'city': data['city'],
            'state': data['state'],
            'country': data['country'],
            'postalcode': data['postalcode'],
            'amount': int(data['quantity']) * int(data['price']), # Use get to avoid KeyError
            'quantity': data['quantity'],
            'token': token, # Use get to avoid KeyError
        }
        # Determine the email template based on the course
        email_template = 'front/email/teacher-registration-email.html'
        html_content = render_to_string(email_template, message_content)
        # Send the email
        send_mail(mail_subject, None, from_email, to_email, html_message=html_content)
        return True
    except BadHeaderError:
        return False
    except Exception as e:
        # Ideally, log the exception for debugging
        logging.error(f"Error sending email: {e} \n{traceback.format_exc()}")
        return False

# Confirmation Whatsapp Notification
def send_tut_whatsapp_notification(data, token):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        contact = data.get('contact', '').strip()  # Ensure contact exists and trim any whitespace
        if not contact:
            logging.error("Contact number missing or not provided.")
            return False

        country_name = data.get('country')
        if not country_name:
            logging.error("Country name missing or not provided.")
            return False

        # 👉🏻 Fetch the country code from the Country model
        try:
            country_obj = Country.objects.get(name=country_name)
            country_code = country_obj.country_code
        except Country.DoesNotExist:
            logging.error(f"No country found in database with name: {country_name}")
            return False

        to_whatsapp_number = f'whatsapp:+{country_code}{contact}'
        #to_whatsapp_number = f'whatsapp:+91{contact}'  # adjust if international

        contentVariables = {
            '1': str(data['quantity']),
            '2': str(token),
            '3': str(data['fullname']),
        }

        client.messages.create(
            content_sid='HX9211c77137804aad2f202f291bf42bda',
            content_variables=json.dumps(contentVariables),
            from_='MG0485ae03bc7fb111cb65a6bd21b10938',
            to=to_whatsapp_number
        )
        return True

    except KeyError as ke:
        logging.error(f"KeyError while processing data for WhatsApp notification: {ke}\n{traceback.format_exc()}")
        return False
    except TwilioRestException as tre:
        logging.error(f"Twilio Error while sending WhatsApp notification: {tre}\n{traceback.format_exc()}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error sending WhatsApp notification: {e}\n{traceback.format_exc()}")
        return False


@login_required(login_url='login')
def teacherSuccessMsg(request, args):
    user_token = get_object_or_404(TeacherUniqueToken, token=args)
    context = {
        'user_token': user_token,
    }

    return render(request, 'front/members/registration/teacher-success.html', context)


def selfTeacherCreation(request, args):
    user_token = get_object_or_404(TeacherUniqueToken, token=args)
    if user_token.count != 0:
        if request.method == 'POST':
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email__exact=email)
                if user.user_type == 'Certified Leader':
                    user.user_type = 'Certified Teacher'
                    user.membership = 'active'
                    user.token = user_token.token
                    user.save()

                    # Create a user membership
                    user_membership = UserMembershipForm()
                    user_membership.user = user
                    user_membership.membership = Membership.objects.get(membership_slug='membership-12-months')
                    user_membership.start_date = datetime.datetime.today()
                    user_membership.expiry_date = user_membership.start_date + timedelta(
                        days=user_membership.membership.membership_duration)
                    user_membership.token = user_token.token
                    user_membership = Subscription.objects.create(
                        user=user_membership.user,
                        membership=user_membership.membership,
                        start_date=user_membership.start_date,
                        expiry_date=user_membership.expiry_date,
                        token=user_membership.token,
                        active=True
                    )
                    user_membership.save()

                    # Reduce Token Count
                    teacher_token = TeacherUniqueToken.objects.get(token=user_token)
                    teacher_token.count = user_token.count - 1
                    teacher_token.save()

                    messages.success(request, 'Congratulations! You are now registered as teacher.')
                    return redirect('login')

                elif user.user_type == 'Certified Master Trainer':
                    messages.error(request, 'You are not allowed to downgrade your designation.')
                    return redirect('login')

                elif user.user_type == 'Certified Teacher':
                    messages.error(request, 'You are already registered as teacher')
                    return redirect('login')

                else:
                    messages.error(request, 'You are not authorized to upgrade your designation, please contact admin.')
                    return redirect('login')

            else:
                messages.error(request,
                               'Oops.. Please use your registered email address or you are not a Certified Leader.')
                return redirect('login')
        else:
            form = SelfTeacherCreationForm()
    else:
        messages.warning(request, '- You have exhausted registration limit.')
        return redirect('login')

    context = {
        'form': form,
    }

    return render(request, 'front/members/teacher-register.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, _('Logged out successfully!'))
    return redirect('login')


def export(request):
    member_resource = CustomUserResource()
    dataset = member_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


@login_required(login_url='login')
def dashboard(request):
    try:
        current_user = request.user
        now = timezone.now()
        user_plan = Subscription.objects.filter(user=current_user, status="Active")
        if user_plan != None:
            for plan in user_plan:
                if plan.active == True:
                    if now > plan.expiry_date:
                        plan.active = False
                        plan.save()
                        return render(request, 'front/members/dashboard.html')

    except Subscription.DoesNotExist:
        user_active_plan = None
    return render(request, 'be/apps/dashboard.html')


# Membership Card Starts Here
PAGE_WIDTH = 85.59 * mm
PAGE_HEIGHT = 53.98 * mm
PAGE_SIZE = PAGE_WIDTH, PAGE_HEIGHT
FONT = "FranklinGothic"
FONT_SIZE = 9
FONT_COLOR = '#0066b3'
TEMPLATE_DIR = settings.BASE_DIR / 'templates' / 'cards'
MEMBERSHIP_CARD_DIR = settings.BASE_DIR / 'media' / 'cards'


def get_template(request):
    current_user = request.user
    if current_user.user_type == 'Certified Leader':
        TEMPLATE_FILE = TEMPLATE_DIR / 'mc-leader.pdf'
    elif current_user.user_type == 'Certified Teacher':
        TEMPLATE_FILE = TEMPLATE_DIR / 'mc-teacher.pdf'
    else:
        TEMPLATE_FILE = TEMPLATE_DIR / 'mc-master.pdf'
    template = TEMPLATE_FILE
    return PdfFileReader(str(template))


def create_info_canvas(mid):
    # Registering Fonts
    pdfmetrics.registerFont(TTFont("FranklinGothic", "FranklinGothic.ttf"))
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=PAGE_SIZE)
    can.setFont(FONT, FONT_SIZE)
    can.setFillColor(HexColor(FONT_COLOR))

    user = get_object_or_404(User, id=mid)

    fullname = f'{user.first_name} {user.last_name}'
    designation = user.user_type
    reg_no = user.registration_no
    user_dp = user.profile_pic.path
    country = user.country.name

    can.drawString(45 * mm, 37.75 * mm, fullname)
    can.drawString(47 * mm, 33.15 * mm, country)
    can.drawString(42 * mm, 28.5 * mm, designation)
    can.drawString(57 * mm, 24 * mm, reg_no)
    can.drawImage(str(user_dp), 11.25 * mm, 20 * mm, width=21 * mm, height=21 * mm)
    can.save()
    packet.seek(0)
    return PdfFileReader(packet)


def create_pdf_file(mid, canvas_info, template):
    page = template.getPage(0)
    page.mergePage(canvas_info.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)

    file_name = MEMBERSHIP_CARD_DIR / f"membership-card-{mid}.pdf"
    with open(file_name, "wb") as file:
        output.write(file)


def remove(request, mid):
    JPG_FILE = MEMBERSHIP_CARD_DIR / f"membership-card-{mid}.jpg"
    # To remove the jpg file from server.
    os.system(f"rm -rf {JPG_FILE}")
    messages.warning(request, 'Successfully deleted your membership card.')
    return redirect('dashboard')


@login_required(login_url='login')
def membershipCard(request, mid):
    subscription_status = Subscription.objects.filter(user=mid, active=True, membership__membership_type='paid')
    if subscription_status:
        current_user = request.user
        JPG_FILE = MEMBERSHIP_CARD_DIR / f"membership-card-{mid}.jpg"
        file_exists = exists(JPG_FILE)  # To check the file is present on server or not
        if file_exists:
            messages.warning(request, 'Your Membership Card already generated.')
        else:
            canvas_info = create_info_canvas(mid)
            # Get PDF File
            template = get_template(request)
            # Merge Canvas with template
            create_pdf_file(mid, canvas_info, template)

            # Store Pdf with convert_from_path function
            PDF_FIlE = MEMBERSHIP_CARD_DIR / f"membership-card-{mid}.pdf"
            images = convert_from_path(PDF_FIlE, dpi=200)
            for i in range(len(images)):
                # Save pages as images in the pdf
                images[i].save(MEMBERSHIP_CARD_DIR / f'membership-card-{mid}.jpg', 'JPEG')
            messages.success(request, 'Membership Card Generated Successfully.')
            # To remove the pdf file from server.
            os.system(f"rm -rf {PDF_FIlE}")

        context = {
            'current_user': current_user,
        }
        return render(request, 'front/members/membership-card.html', context)

    else:
        JPG_FILE = MEMBERSHIP_CARD_DIR / f"membership-card-{mid}.jpg"
        file_exists = exists(JPG_FILE)
        if file_exists:
            # To remove the pdf file from server.
            os.remove(JPG_FILE)
        else:
            pass
        return redirect('membership-plan')


# Membership Card Ends Here

# Visiting Card Starts Here


VC_PAGE_WIDTH = 85.59 * mm
VC_PAGE_HEIGHT = 53.98 * mm
VC_PAGE_SIZE = PAGE_WIDTH, PAGE_HEIGHT


def get_vc_template(request):
    template = TEMPLATE_DIR / 'vc-template.pdf'
    return PdfFileReader(str(template))


def create_vc_canvas(mid):
    user = get_object_or_404(User, id=mid)

    fullname = f'{user.first_name} {user.last_name}'
    designation = user.user_type
    contact_number = user.contact_number
    email = user.email
    # website = user.website_url
    # services = user.services

    # Registering Fonts
    pdfmetrics.registerFont(TTFont("FuturaHeavyBT", "FuturaHeavyBT.ttf"))
    pdfmetrics.registerFont(TTFont("FuturaBkBT", "FuturaBkBT.ttf"))
    pdfmetrics.registerFont(TTFont("Swis721CnBT", "Swis721CnBT.ttf"))
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=VC_PAGE_SIZE)

    can.setFont('FuturaHeavyBT', 9)
    can.setFillColor(HexColor('#034ea2'))
    can.drawString(25 * mm, 38 * mm, fullname)

    can.setFont('FuturaBkBT', 7)
    can.setFillColor(HexColor('#58595b'))
    can.drawString(47 * mm, 33.15 * mm, designation)
    can.drawString(42 * mm, 28.5 * mm, contact_number)
    can.drawString(57 * mm, 24 * mm, email)
    # can.drawString(60 * mm, 20 * mm, website)

    can.setFont('Swis721CnBT', 6)
    can.setFillColor(HexColor('#58595b'))
    # can.drawString(20 * mm, 15 * mm, services)

    can.save()
    packet.seek(0)
    return PdfFileReader(packet)


def create_vc_pdf_file(mid, canvas_info, template):
    page = template.getPage(0)
    page.mergePage(canvas_info.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)

    file_name = MEMBERSHIP_CARD_DIR / f"visiting-card-{mid}.pdf"
    with open(file_name, "wb") as file:
        output.write(file)


def removeVC(request, mid):
    VC_FILE = MEMBERSHIP_CARD_DIR / f"visiting-card-{mid}.pdf"
    # To remove the pdf file from server.
    os.system(f"rm -rf {VC_FILE}")
    messages.warning(request, 'Successfully deleted your visiting card.')
    return redirect('dashboard')


@login_required(login_url='login')
def visitingCard(request, mid):
    subscription_status = Subscription.objects.filter(user=mid, active=True)
    if subscription_status:
        current_user = request.user
        PDF_FIlE = MEMBERSHIP_CARD_DIR / f"visiting-card-{mid}.pdf"
        file_exists = exists(PDF_FIlE)  # To check the file is present on server or not
        if file_exists:
            messages.warning(request, 'Your Visiting Card already generated.')
        else:
            canvas_info = create_vc_canvas(mid)
            # Get PDF File
            template = get_vc_template(request)
            # Merge Canvas with template
            create_vc_pdf_file(mid, canvas_info, template)
            messages.success(request, 'Visiting Card Generated Successfully.')

        context = {
            'current_user': current_user,
        }
        return render(request, 'front/members/visiting-card.html', context)

    else:
        PDF_FIlE = MEMBERSHIP_CARD_DIR / f"visiting-card-{mid}.pdf"
        file_exists = exists(PDF_FIlE)
        if file_exists:
            # To remove the pdf file from server.
            os.remove(PDF_FIlE)
        else:
            pass
        return redirect('membership-plan')


# Visiting Card Starts Ends Here

# Certified Leader Certificate Starts Here
CLYL_PAGE_WIDTH = 296.84 * mm
CLYL_PAGE_HEIGHT = 210.06 * mm
CLYL_PAGE_SIZE = CLYL_PAGE_WIDTH, CLYL_PAGE_HEIGHT
CLYL_FONT = "Lucida Calligraphy"
CLYL_FONT_SIZE = 15
CLYL_FONT_COLOR = '#9b4e3e'
CLYL_FONT_DESIGNATION = "Arial"
CLYL_FONT_SIZE_DESIGNATION = 12
CLYL_FONT_COLOR_DESIGNATION = '#000000'
LEADER_CERTIFICATE_DIR = settings.BASE_DIR / 'media' / 'certificates' / 'leader'


def get_clylc_template(request):
    template = TEMPLATE_DIR / 'clylc-template.pdf'
    return PdfFileReader(str(template))


def create_clylc_canvas(mid):
    user = get_object_or_404(User, id=mid)

    fullname = f'{user.first_name} {user.last_name}'
    if user.user_type == 'Certified Master Trainer':
        designation = 'Master Trainer'
    else:
        designation = 'Teacher'

    # Registering Fonts
    pdfmetrics.registerFont(TTFont("Lucida Calligraphy", "LucidaCalligraphy.ttf"))
    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=CLYL_PAGE_SIZE)

    can.setFont(CLYL_FONT, CLYL_FONT_SIZE)
    can.setFillColor(HexColor(CLYL_FONT_COLOR))
    can.drawString(210 * mm, 29 * mm, fullname)

    can.setFont(CLYL_FONT_DESIGNATION, CLYL_FONT_SIZE_DESIGNATION)
    can.setFillColor(HexColor(CLYL_FONT_COLOR_DESIGNATION))
    can.drawString(210 * mm, 22.5 * mm, designation)

    can.save()
    packet.seek(0)
    return PdfFileReader(packet)


def create_clylc_pdf_file(mid, canvas_info, template):
    page = template.getPage(0)
    page.mergePage(canvas_info.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)

    file_name = LEADER_CERTIFICATE_DIR / f"leader-certificate-{mid}.pdf"
    with open(file_name, "wb") as file:
        output.write(file)


def removeCLYLC(request, mid):
    CLYLC_PDF_FILE = LEADER_CERTIFICATE_DIR / f"leader-certificate-{mid}.pdf"
    os.system(f"rm -rf {CLYLC_PDF_FILE}")  # To remove the pdf file from server.
    CLYLC_JPG_FILE = LEADER_CERTIFICATE_DIR / f"leader-certificate-{mid}.jpg"
    os.system(f"rm -rf {CLYLC_JPG_FILE}")  # To remove the jpg file from server.
    messages.warning(request, 'Successfully deleted the leader certificate.')
    return redirect('dashboard')


@login_required(login_url='login')
def leaderCertificate(request, mid):
    current_user = request.user
    PDF_FIlE = LEADER_CERTIFICATE_DIR / f"leader-certificate-{mid}.pdf"
    file_exists = exists(PDF_FIlE)  # To check the file is present on server or not
    if file_exists:
        messages.warning(request, 'Your leader certificate already generated.')
    else:
        canvas_info = create_clylc_canvas(mid)
        # Get PDF File
        template = get_clylc_template(request)
        # Merge Canvas with template
        create_clylc_pdf_file(mid, canvas_info, template)

        # Store Pdf with convert_from_path function
        PDF_FIlE = LEADER_CERTIFICATE_DIR / f"leader-certificate-{mid}.pdf"
        images = convert_from_path(PDF_FIlE, dpi=200)
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save(LEADER_CERTIFICATE_DIR / f'leader-certificate-{mid}.jpg', 'JPEG')
        messages.success(request, 'Leader Certificate Generated Successfully.')

    context = {
        'current_user': current_user,
    }
    return render(request, 'front/members/certificates/leader-certificate.html', context)


# Certified Leader Certificate Ends Here

@login_required(login_url='login')
def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Successfully updated your details.'))
            return redirect('dashboard')
    else:
        form = EditProfileForm(instance=request.user)

    data = {
        'form': form,
    }
    return render(request, 'front/members/edit-profile.html', data)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            full_name = user.first_name + user.last_name
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message_content = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email,)
            html_content = render_to_string('front/members/passwords/reset_password_email.html', message_content)

            if email:
                try:
                    send_mail(mail_subject, None, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Password reset email has been sent to your email address.')
                return redirect('login')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'front/members/passwords/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'front/members/passwords/resetPassword.html')


# Dashboard Change Password

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(email__exact=request.user.email)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'front/members/passwords/change_password.html')


def workinProgress(request):
    return render(request, 'front/wip.html')


@superuser_required
def userListView(request):
    currentUser = request.user

    # Check user permissions
    if not (currentUser.is_superuser or currentUser.is_admin):
        messages.error(request, 'You are not allowed to view this page!')
        return redirect('dashboard')

    # Handle search
    userSearch = request.POST.get('userSearch', '') or request.GET.get('userSearch', '')
    if userSearch:
        allUsers = Account.objects.filter(
            Q(first_name__icontains=userSearch) |
            Q(last_name__icontains=userSearch) |
            Q(email__icontains=userSearch) |
            Q(contact_number__icontains=userSearch)
        ).order_by('-date_joined')
    else:
        allUsers = Account.objects.all().order_by('-date_joined')

    # Handle pagination
    items_per_page = int(request.GET.get('items', 30))  # Defaulted to 10
    paginator = Paginator(allUsers, items_per_page)
    page_number = request.GET.get('page')
    paged_all_users = paginator.get_page(page_number)

    context = {
        'allUsers': paged_all_users,
        'items_per_page': items_per_page,
        'userSearch': userSearch,
    }
    return render(request, 'be/apps/users/account/read.html', context)


@login_required(login_url='login')
def userView(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access the profile.")
        return redirect('login')  # Redirect to login page

    if request.user.id != pk:
        messages.error(request, "You are not allowed to do this.")
        # Redirect them to their own profile page
        return redirect(reverse('userView', args=[request.user.id]))

    try:
        userAccount = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        userAccount = None

    context = {
        'userAccount': userAccount,
    }
    return render(request, 'be/apps/users/account/view.html', context)


@login_required(login_url='login')
def userAddView(request):
    if request.method == 'POST':
        userForm = AccountAddForm(request.POST)
        if userForm.is_valid():
            first_name = userForm.cleaned_data['first_name']
            last_name = userForm.cleaned_data['last_name']
            email = userForm.cleaned_data['email']
            password = userForm.cleaned_data['password']
            phone_number = userForm.cleaned_data['phone_number']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,
            )
            user.phone_number = phone_number
            user.status = 'Active'
            user.save()

            # Create Address instance for the new user
            UserProfile.objects.create(user=user)

            # Create User Image instance for the new user
            UserImage.objects.create(user=user)

            # Create Social Profile instance for the new user
            SocialProfile.objects.create(user=user)

            # Create Address instance for the new user
            Address.objects.create(user=user)

            # Create Newsletter instance for the new user
            Newsletter.objects.create(user=user)

            # Create AccountToken instance for the new user
            AccountToken.objects.create(user=user)

            messages.success(request, 'Your account has been created.')
            return redirect('userList')
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        userForm = AccountAddForm()

    context = {
        'userForm': userForm,
    }
    return render(request, 'be/apps/users/account/create.html', context)


@login_required(login_url='login')
def userEditView(request, pk):
    userAccount = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        userForm = EditProfileForm(request.POST, request.FILES, instance=userAccount)
        if userForm.is_valid():
            if userForm.has_changed():
                userForm.save()
                messages.success(request, 'User account has been updated.')
            else:
                messages.info(request, 'Nothing has changed.')
            return redirect(reverse('userView', args=[userAccount.pk]))
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        userForm = EditProfileForm(instance=userAccount)

    context = {
        'userAccount': userAccount,
        'userForm': userForm,
    }
    return render(request, 'be/apps/users/account/update.html', context)


@login_required(login_url='login')
def userDeleteView(request, pk):
    currentUser = request.user
    userAccount = get_object_or_404(Account, id=pk)
    if currentUser.is_superuser or currentUser.is_admin:
        if currentUser.id == int(userAccount.id):
            messages.warning(request, 'You can\'t delete your own account')
        else:
            if request.method == "POST":
                userAccount.is_deleted = True
                userAccount.deleted_at = timezone.now()
                userAccount.save()
                messages.success(request, 'You have successfully deleted the account!')
                return redirect('userList')
    else:
        messages.error(request, 'You are not allowed to do this!')
    context = {
        'userAccount': userAccount,
    }
    return render(request, 'be/apps/users/account/delete.html', context)