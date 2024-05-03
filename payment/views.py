from urllib import request
import stripe
import secrets
import urllib
import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from settings.models import WebSettings, Country
from .forms import LY2Form, cttForm, blcIndForm
from .models import ly2Transaction, blcTransaction, cttTransaction, indTraining

# WhatsApp Twilio
from twilio.rest import Client
from settings.models import Twilio
from twilio.base.exceptions import TwilioRestException

# Email
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect


# 👉🏻 Google reCaptcha Validation
def validate_recaptcha(recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': WebSettings.private_key,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result['success']


# 👉🏻 LY 2 Payment Process Starts Here
ly2_price_map = {
    'LY 2.0 Season 6 Live': 125,
    'LY 2.0 Bundle Download': 297,
    'LY 2.0 Season 5 Download': 69.95,
    'LY 2.0 Season 4 Download': 69.95,
    'LY 2.0 Season 3 Download': 69.95,
    'LY 2.0 Season 2 Download': 69.95,
    'LY 2.0 Season 1 Download': 69.95,
}
def ly2charge(request):
    if request.method != 'POST':
        # 👉🏻 Handle non-POST requests if needed or just return a response.
        return redirect(reverse('ly2'))

    # 👉🏻 Extracting data from POST request
    course = request.POST.get('course', '')
    amount = ly2_price_map.get(course, 0)

    print(amount)

    form_fields = ['fullname', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'contact', 'information']
    data = {field: request.POST.get(field, '') for field in form_fields}

    # 👉🏻 reCAPTCHA Validation
    if not validate_recaptcha(request.POST.get('g-recaptcha-response')):
        messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return redirect('ly2')

    # 👉🏻 Stripe customer creation and charging
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
            amount=int(amount * 100),
            currency='usd',
            description=course,
        )
    except stripe.error.StripeError as e:
        logging.error(f"Stripe Error: {e}")
        messages.error(request, f"Stripe Error: {e}")
        return redirect(reverse('ly2') + '#payment')

    # 👉🏻 Storing the transaction
    ly2_transaction = create_ly2_transaction(data, amount, course)
    ly2_transaction.save()

    # 👉🏻 Send Email
    if not send_ly2_signup_email(data, course):
        messages.error(request, 'Error sending the email.')
        return redirect('ly2success')

    return redirect('ly2success')


# Create a LY2 Transaction
def create_ly2_transaction(data, amount, course):
    token = secrets.token_urlsafe(16)
    transaction = ly2Transaction(
        course=course,
        full_name=data['fullname'],
        email=data['email'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        country=data['country'],
        postalcode=data['postalcode'],
        price=amount,
        contact=data['contact'],
        information=data['information'],
        token=token,
    )
    return transaction


ly2_email_template_map = {
    # 'LY 2.0 Season 5 Live': 'front/email/ly2s5-transaction-email.html',
    'LY 2.0 Bundle Download': 'front/email/ly2-all-transaction-email.html',
    'LY 2.0 Season 1 Download': 'front/email/ly2s1-transaction-email.html',
    'LY 2.0 Season 2 Download': 'front/email/ly2s2-transaction-email.html',
    'LY 2.0 Season 3 Download': 'front/email/ly2s3-transaction-email.html',
    'LY 2.0 Season 4 Download': 'front/email/ly2s4-transaction-email.html',
    'LY 2.0 Season 5 Download': 'front/email/ly2s5-transaction-email.html',
}

def send_ly2_signup_email(data, course):
    try:
        # Subject and email receivers
        mail_subject = f'{data["fullname"]} signed up for {course}'
        from_email = f'Laughter Yoga International <{settings.DEFAULT_FROM_EMAIL}>'
        to_email = (data['email'], 'Laughter Yoga International <help@laughteryoga.org>')

        # Determine the amount
        if course in ly2_price_map:
            amount = ly2_price_map[course]

        # Message content
        message_content = {
            'course': course,
            'fullname': data['fullname'],
            'email': data['email'],
            'address': data['address'],
            'city': data['city'],
            'state': data['state'],
            'country': data['country'],
            'postalcode': data['postalcode'],
            'amount': amount,
            # defaulting amount based on course if not provided
            'contact': data['contact'],
            'information': data['information'],
        }

        # Determine the email template based on the course
        email_template = ly2_email_template_map.get(course)
        html_content = render_to_string(email_template, message_content)

        # Send the email
        send_mail(mail_subject, None, from_email, to_email, html_message=html_content)

        return True
    except BadHeaderError:
        return False
    except Exception as e:
        # Ideally, log the exception for debugging
        print(f"Error sending email: {e}")
        return False


def ly2successMsg(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('ly2')
    context = {}
    return render(request, 'front/payment/success.html', context)
# 👉🏻 LY 2 Payment Process Ends Here


# 👉🏻 BLC Course Payment Starts Here
price_map = {
    'Basic Learning Course': 84,
    'Basic Learning Course + Certified Leader Training': 233
}

def blccharge(request):
    if request.method != 'POST':
        # 👉🏻 Handle non-POST requests if needed or just return a response.
        return redirect(reverse('basic-learning-course'))

    # 👉🏻 Extracting data from POST request
    course = request.POST.get('course', '')
    amount = price_map.get(course, 0)

    form_fields = ['fullname', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'contact', 'information']
    data = {field: request.POST.get(field, '') for field in form_fields}

    # 👉🏻 reCAPTCHA Validation
    if not validate_recaptcha(request.POST.get('g-recaptcha-response')):
        messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return redirect('basic-learning-course')

    # 👉🏻 Stripe customer creation and charging
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
            amount=int(amount) * 100,
            currency='usd',
            description=course,
        )
    except stripe.error.StripeError as e:
        logging.error(f"Stripe Error: {e}")
        messages.error(request, f"Stripe Error: {e}")
        return redirect(reverse('basic-learning-course') + '#payment')

    # 👉🏻 Storing the transaction
    blc_transaction = create_blc_transaction(data, amount, course)
    blc_transaction.save()

    # 👉🏻 Send Email
    if not send_confirmation_email(data, course):
        messages.error(request, 'Error sending the email.')
        return redirect('blcsuccess')

    # 👉🏻 Send Whatsapp Notification
    if not send_confirmation_notification(data, course):
        messages.error(request, 'Error sending the WhatsApp notification')
        return redirect('blcsuccess')

    return redirect('blcsuccess')


# 👉🏻 DB Entry Functionality
def create_blc_transaction(data, amount, course):
    token = secrets.token_urlsafe(16)
    transaction = blcTransaction(
        course=course,
        full_name=data['fullname'],
        email=data['email'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        country=data['country'],
        postalcode=data['postalcode'],
        price=amount,
        contact=data['contact'],
        information=data['information'],
        token=token,
    )
    return transaction


# 👉🏻 Confirmation Email Functionality
def send_confirmation_email(data, course):
    try:
        # Subject and email receivers
        mail_subject = f'{data["fullname"]} signed up for {course}'
        from_email = f'Laughter Yoga International <{settings.DEFAULT_FROM_EMAIL}>'
        to_email = (data['email'], 'Laughter Yoga International <help@laughteryoga.org>')

        # Message content
        message_content = {
            'course': course,
            'fullname': data['fullname'],
            'email': data['email'],
            'address': data['address'],
            'city': data['city'],
            'state': data['state'],
            'country': data['country'],
            'postalcode': data['postalcode'],
            'amount': data.get('amount', 84 if course == 'Basic Learning Course' else 233),
            # defaulting amount based on course if not provided
            'contact': data['contact'],
            'information': data['information'],
        }

        # Determine the email template based on the course
        email_template = 'front/email/blc-transaction-email.html' if course == 'Basic Learning Course' else 'front/email/combo-transaction-email.html'

        html_content = render_to_string(email_template, message_content)

        # Send the email
        send_mail(mail_subject, None, from_email, to_email, html_message=html_content)

        return True
    except BadHeaderError:
        return False
    except Exception as e:
        # Ideally, log the exception for debugging
        print(f"Error sending email: {e}")
        return False

# 👉🏻 Confirmation WhatsApp notification functionality
def send_confirmation_notification(data, course):
    try:
        # 👉🏻 Sending WhatsApp Message
        client = Client(Twilio.accountSID, Twilio.authToken)

        # 👉🏻 Retrieving the contact number and country name from the form data
        contact = data.get('contact')
        country_name = data.get('country')  # This gets the selected country's name from the dropdown

        # 👉🏻 Fetch the country code from the Country model
        try:
            country_obj = Country.objects.get(name=country_name)
            country_code = country_obj.country_code
        except Country.DoesNotExist:
            logging.error(f"No country found in database with name: {country_name}")
            return False

        #to_whatsapp_number = f'whatsapp:+{country_code}{contact}'
        to_whatsapp_number = f'whatsapp:+91{contact}' # 👉🏻 This code is only applicable for localhost

        # 👉🏻 Mapping of course to respective content_sid
        course_message_map = {
            'Basic Learning Course': 'HX1a0b91c4b72f85e3f78bb4038fbc344c',
            'Basic Learning Course + Certified Leader Training': 'HXd9b6777a4cfde445914e533cfda3a448'
        }
        content_sid = course_message_map.get(course)

        whatsApp_link = 'https://chat.whatsapp.com/LF9c6I9pvcPCNyDzzx0oMM'
        blc_usa_date = 'April 2024: 7th, 8th, 9th, 10th, 11th, 12th'
        blc_usa_time ='7:30 pm PST/PDT | 8:30 pm MST/MT | 9:30 pm CST/CT | 10:30 pm EST/ET'
        blc_ind_date='April 2024: 8th, 9th, 10th, 11th, 12th, 13th'
        blc_ind_time='Live at 8 am'

        combo_usa_date = 'April 2024: 7th, 8th, 9th, 10th, 11th, 12th, 14th, 15th, 16th, 17th, 18th, 19th'
        combo_usa_time = '7:30 pm PST/PDT | 8:30 pm MST/MT | 9:30 pm CST/CT | 10:30 pm EST/ET'
        combo_ind_date = 'April 2024: 8th, 9th, 10th, 11th, 12th, 13th, 15th, 16th, 17th, 18th, 19th, 20th'
        combo_ind_time = 'Live at 8 am'

        blc_contentVariables = {
            '1': str(whatsApp_link),
            '2': str(blc_usa_date),
            '3': str(blc_usa_time),
            '4': str(blc_ind_date),
            '5': str(blc_ind_time),
        }

        combo_contentVariables = {
            '1': str(whatsApp_link),
            '2': str(combo_usa_date),
            '3': str(combo_usa_time),
            '4': str(combo_ind_date),
            '5': str(combo_ind_time),
        }

        course_content_variables_map = {
            'Basic Learning Course': blc_contentVariables,
            'Basic Learning Course + Certified Leader Training': combo_contentVariables
        }

        content_variables = course_content_variables_map.get(course)

        if not content_sid:
            logging.error(f"No content_sid found for the course: {course}")
            return False

        client.messages.create(
            content_sid=content_sid,
            content_variables=json.dumps(content_variables),
            from_='MG0485ae03bc7fb111cb65a6bd21b10938',
            to=to_whatsapp_number,
        )
        return True


    except KeyError as ke:
        logging.error(f"KeyError while processing data for WhatsApp notification: {ke}")
        return False

    except TwilioRestException as tre:
        logging.error(f"Twilio Error while sending WhatsApp notification: {tre}")
        return False

    except Exception as e:
        # 👉🏻 General exception logging
        logging.error(f"Error sending WhatsApp notification: {e}")
        return False

def blcsuccessMsg(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('basic-learning-course')
    context = {}
    return render(request, 'front/payment/blc-success.html', context)
# 👉🏻 BLC Course Payment Ends Here 👆🏻

# Certified Teacher Training (CTT) Payment Process Starts Here
def teachertcharge(request):
    amount = 0
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        postalcode = request.POST['postalcode']
        amount = 89500
        contact = request.POST['contact']
        information = request.POST['information']

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
            customer = stripe.Customer.create(
                name=fullname,
                email=email,
                address={
                    'city': city,
                    'country': country,
                    'line1': address,
                    'postal_code': postalcode,
                    'state': state,
                },
                source=request.POST['stripeToken'],
            )
            stripe.Charge.create(
                customer=customer,
                amount=amount,
                currency='usd',
                description='5 Day Teacher Training Fee',
            )

            # Create a Teacher Training Transaction
            ctt_transaction = cttForm()
            ctt_transaction.fullname = fullname
            ctt_transaction.email = email
            ctt_transaction.address = address
            ctt_transaction.city = city
            ctt_transaction.state = state
            ctt_transaction.country = country
            ctt_transaction.postalcode = postalcode
            ctt_transaction.price = amount / 100
            ctt_transaction.contact = contact
            ctt_transaction.information = information
            ctt_transaction.token = secrets.token_urlsafe(16)
            ctt_submission = cttTransaction.objects.create(
                full_name=ctt_transaction.fullname,
                email=ctt_transaction.email,
                address=ctt_transaction.address,
                city=ctt_transaction.city,
                state=ctt_transaction.state,
                country=ctt_transaction.country,
                postalcode=ctt_transaction.postalcode,
                price=ctt_transaction.price,
                contact=ctt_transaction.contact,
                information=ctt_transaction.information,
                token=ctt_transaction.token,
            )
            ctt_submission.save()

            # Sending Email
            mail_subject = fullname + ' signed up for 5 Day Teacher Training Program'
            message_content = {
                'fullname': fullname,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'country': country,
                'postalcode': postalcode,
                'amount': amount / 100,
                'contact': contact,
                'information': information,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/ctt-transaction-email.html', message_content)
            if fullname and email and address and city and state and country and postalcode and amount and contact and information:
                try:
                    send_mail(mail_subject, None, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                return redirect(reverse('cttsuccess', args=[ctt_transaction.token]))
            else:
                return HttpResponse('Make sure all fields are entered and valid.')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('teacher-training')


def teachertsuccessMsg(request, args):
    user_token = get_object_or_404(cttTransaction, token=args)
    context = {
        'user_token': user_token,
    }

    return render(request, 'front/payment/ctt-success.html', context)
# Certified Teacher Training (CTT) Payment Process Ends Here


# Indian Training Payment Starts Here

def indTrainingCharge(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        contact = request.POST['contact']
        amount = 590
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
            try:
                # Create a PaymentIntent with the order amount and currency
                intent = stripe.PaymentIntent.create(
                    amount=59000, #Rs 590.00
                    currency='inr',
                    automatic_payment_methods={
                        'enabled': True,
                    },
                )
                return JsonResponse({
                    'clientSecret': intent['client_secret']
                })
            except Exception as e:
                return JsonResponse(error=str(e)), 403



            # Create a BLC India Training Transaction
            blcInd_transaction = blcIndForm()
            blcInd_transaction.fullname = fullname
            blcInd_transaction.email = email
            blcInd_transaction.price = amount
            blcInd_transaction.contact = contact
            blcInd_transaction.token = token

            blcInd_submission = indTraining.objects.create(
                full_name=blcInd_transaction.fullname,
                email=blcInd_transaction.email,
                price=blcInd_transaction.price,
                contact=blcInd_transaction.contact,
                token=blcInd_transaction.token,
                instamojo_response=response,
            )
            blcInd_submission.save()
            return redirect(response['payment_request']['longurl'])

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('blc-india')
    else:
        return redirect('blc-india')


def blcIndsuccess(request):
    payment_request_id = request.GET.get('payment_request_id')
    blc_ind = indTraining.objects.get(token=payment_request_id)

    # Sending Email
    mail_subject = blc_ind.full_name + ' signed up for BLC Indian Training'
    message_content = {
        'fullname': blc_ind.full_name,
        'email': blc_ind.email,
        'amount': blc_ind.price,
        'contact': blc_ind.contact,
    }
    from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
    to_email = (blc_ind.email, 'Laughter Yoga International <help@laughteryoga.org>')
    html_content = render_to_string('front/email/blc-ind-transaction-email.html', message_content)
    try:
        send_mail(mail_subject, None, from_email, to_email, html_message=html_content)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    return render(request, 'front/payment/blc-ind-success.html')


@csrf_exempt
def wcSuccess(request):
        # mail_subject =' signed up for World Conference in India'
        # message_content = {
        #     'name': userToken.name,
        #     'email': userToken.email,
        #     'phone': userToken.phone,
        #     'country': userToken.country,
        #     'status': userToken.status,
        #     'amount': userToken.amount/100,
        # }
        # from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
        # to_email = (userToken.email, 'Laughter Yoga International <help@laughteryoga.org>')
        # html_content = render_to_string('front/email/wc-transaction-email.html', message_content)
        # try:
        #     send_mail(mail_subject, None, from_email, to_email, html_message=html_content)
        # except BadHeaderError:
        #     return HttpResponse('Invalid header found.')
    return render(request, 'front/payment/rpSuccess.html')