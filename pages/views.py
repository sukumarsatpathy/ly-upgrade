import mimetypes
import os
import urllib
import json
import secrets
import logging
from os.path import exists
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.decorators import superuser_required, user_has_active_membership
from .models import Diary, generalResearch, laughterBlogsCat, laughterBlogs, GetInvolved
from .forms import DiaryForm, BlogsForm, gResearchForm, GetInvolvedForm, UserForm
from settings.models import State, City
# from .filters import RegisteredProfessionals
from news.models import News
from club.models import Club
from club.forms import ClubFinderForm
from testimonial.models import Testimonial
from training.models import Training
from settings.models import WebSettings, StripeGateway
# from .forms import UserForm
from report.forms import ContactForm, InfoBookletForm, LYTourEnquiryForm, ZoomLCForm
from report.models import Contact, InfoBooklet, TrainerProfileEnquiry, LYTourEnquiry, ZoomLCEnquiry, SpiritualRetreat
from settings.models import Country
# WhatsApp Twilio
from twilio.rest import Client
# from core.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
from twilio.base.exceptions import TwilioRestException
# Email
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


User = get_user_model()


def twilioDomainVerification(request):
    return render(request, '5c84d2c89a4d975aff2361cd41d356ec.html')


def home(request):
    home_get_involved = GetInvolved.objects.filter(status='Published').order_by('created_date')
    home_testimonials = Testimonial.objects.filter(status="Published").order_by('-created_date')[:6]
    home_news = News.objects.filter(status="Published").order_by('-created_date')[:6]
    context = {
        'home_get_involved': home_get_involved,
        'home_testimonials': home_testimonials,
        'home_news': home_news,
    }
    return render(request, 'front/pages/home.html', context)


def aboutly(request):
    return render(request, 'front/pages/about-laughter-yoga.html')


def downloadInfoBooklet(request):
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        country = request.POST['country']

        # Create an Info Booklet Entry
        info_booklet = InfoBookletForm()
        info_booklet.full_name = full_name
        info_booklet.email = email
        info_booklet.country = country
        form_submission = InfoBooklet.objects.create(
            full_name=info_booklet.full_name,
            email=info_booklet.email,
            country=info_booklet.country,
        )
        form_submission.save()

    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'info-booklet.pdf'
    # Define the full file path
    filepath = BASE_DIR + '/media/download_files/' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def aboutlc(request):
    return render(request, 'front/pages/about-laughter-club.html')


# World Laughter Day Views Starts Here
def aboutWld(request):
    return render(request, 'front/pages/about-world-laughter-day.html')


def wldMessage(request):
    return render(request, 'front/pages/wld/wld-message.html')


def wldRoundLogo(request):
    return render(request, 'front/pages/wld/wld-round-logo.html')


def wldBluebgLogo(request):
    return render(request, 'front/pages/wld/wld-blue-bg-logo.html')


def wldBanner(request):
    return render(request, 'front/pages/wld/wld-banner.html')


def schoolChildren(request):
    site_key = WebSettings.public_key
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a School Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='School',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New School Children Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('school-children')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('school-children')

    context = {
        'site_key': site_key,
    }

    return render(request, 'front/pages/ly-with-school-children.html', context)


def business(request):
    site_key = WebSettings.public_key
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a School Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Business',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Business Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('business')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('business')

    context = {
        'site_key': site_key,
    }

    return render(request, 'front/pages/ly-in-business.html', context)


def depression(request):
    return render(request, 'front/pages/ly-depression.html')


def specialNeeds(request):
    site_key = WebSettings.public_key
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a School Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Special Needs',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Special Needs Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('special-needs')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('special-needs')

    context = {
        'site_key': site_key,
    }

    return render(request, 'front/pages/special-needs.html', context)


def seniors(request):
    return render(request, 'front/pages/seniors.html')


def cancer(request):
    return render(request, 'front/pages/cancer.html')


def yogaPlusly(request):
    return render(request, 'front/pages/yoga-plus-laughter-yoga.html')


def lyResearch(request):
    return render(request, 'front/pages/laughter-yoga-research.html')


def aboutTraining(request):
    return render(request, 'front/pages/about-training.html')


def teacherTraining(request):
    all_countries = Country.objects.all()
    stripe_public_key = StripeGateway.public_key
    site_key = WebSettings.public_key

    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a Teacher Training Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Teacher Training',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Teacher Training Course Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('teacher-training')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('teacher-training')

    context = {
        'all_countries': all_countries,
        'stripe_public_key': stripe_public_key,
        'site_key': site_key,
    }

    return render(request, 'front/pages/teacher-training-by-drk.html', context)


def basicLearningCourse(request):
    all_countries = Country.objects.all()
    stripe_public_key = StripeGateway.public_key
    site_key = WebSettings.public_key

    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a School Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Basic Learning Course',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Basic Learning Course Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                    messages.success(request, 'Thank you. We have received your enquiry.')
                    return redirect('blc-success')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('basic-learning-course')

    context = {
        'all_countries': all_countries,
        'stripe_public_key': stripe_public_key,
        'site_key': site_key,
    }
    return render(request, 'front/pages/basic-learning-course.html', context)


def blcSuccess(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('basic-learning-course')
    context = {}
    return render(request, 'front/pages/success/blc-thankyou.html', context)


def mentalHealth(request):
    all_countries = Country.objects.all()
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    site_key = settings.RECAPTCHA_PUBLIC_KEY

    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a School Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Basic Learning Course',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Basic Learning Course Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('basic-learning-course')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('basic-learning-course')

    context = {
        'all_countries': all_countries,
        'stripe_public_key': stripe_public_key,
        'site_key': site_key,
    }
    return render(request, 'front/pages/mental-health.html', context)


def blcIndia(request):
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a School Contact Entry
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Basic Learning Course',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Basic Learning Course India Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/blc-ind-enquiry-email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                    messages.success(request, 'Thank you. We have received your enquiry.')
                    return redirect('blc-ind-success')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('blc-india')
    context = {
        'site_key': site_key,
    }
    return render(request, 'front/pages/basic-learning-course-india.html', context)


def blcIndSuccess(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('blc-india')
    context = {}
    return render(request, 'front/pages/success/blc-ind-thankyou.html', context)


def indiaTour(request):
    # site_key = settings.RECAPTCHA_PUBLIC_KEY
    # if request.method == 'POST':
    #     full_name = request.POST['name']
    #     email = request.POST['email']
    #     contact = request.POST['contact']
    #
    #     ''' Begin reCAPTCHA validation '''
    #     recaptcha_response = request.POST.get('g-recaptcha-response')
    #     url = 'https://www.google.com/recaptcha/api/siteverify'
    #     values = {
    #         'secret': settings.RECAPTCHA_PRIVATE_KEY,
    #         'response': recaptcha_response
    #     }
    #     data = urllib.parse.urlencode(values).encode()
    #     req = urllib.request.Request(url, data=data)
    #     response = urllib.request.urlopen(req)
    #     result = json.loads(response.read().decode())
    #     ''' End reCAPTCHA validation '''
    #
    #     if result['success']:
    #         # Contact Form submission
    #         tour_form = LYTourEnquiryForm()
    #         tour_form.full_name = full_name
    #         tour_form.email = email
    #         tour_form.contact = contact
    #         form_submission = LYTourEnquiry.objects.create(
    #             full_name=tour_form.full_name,
    #             email=tour_form.email,
    #             contact=tour_form.contact,
    #         )
    #         form_submission.save()
    #
    #         # Sending Email
    #         mail_subject = full_name + ' Enrolled for LY Tour '
    #         message = 'New Enrollment'
    #         message_content = {
    #             'full_name': full_name,
    #             'email': email,
    #             'contact': contact,
    #         }
    #         from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
    #         to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
    #         html_content = render_to_string('front/email/ly_tour_email.html', message_content)
    #         if full_name and email and contact:
    #             try:
    #                 send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
    #             except BadHeaderError:
    #                 return HttpResponse('Invalid header found.')
    #             messages.success(request, 'Thank you for your enrollment. We have successfully booked your spot.')
    #             return redirect('india-tour')
    #         else:
    #             return HttpResponse('Make sure all fields are entered and valid.')
    #
    #     else:
    #         messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    #         return redirect('india-tour')
    #
    # context = {
    #     'site_key': site_key,
    # }
    #
    # return render(request, 'front/pages/free-online-yoga-training.html', context)
    return redirect('free-online-yoga-training')


def freeOnlineYogaTraining(request):
    return render(request, 'front/pages/free-online-yoga-training.html')


def jaipurTour(request):
    # site_key = settings.RECAPTCHA_PUBLIC_KEY
    # if request.method == 'POST':
    #     full_name = request.POST['name']
    #     email = request.POST['email']
    #     contact = request.POST['contact']
    #
    #     ''' Begin reCAPTCHA validation '''
    #     recaptcha_response = request.POST.get('g-recaptcha-response')
    #     url = 'https://www.google.com/recaptcha/api/siteverify'
    #     values = {
    #         'secret': settings.RECAPTCHA_PRIVATE_KEY,
    #         'response': recaptcha_response
    #     }
    #     data = urllib.parse.urlencode(values).encode()
    #     req = urllib.request.Request(url, data=data)
    #     response = urllib.request.urlopen(req)
    #     result = json.loads(response.read().decode())
    #     ''' End reCAPTCHA validation '''
    #
    #     if result['success']:
    #         # Contact Form submission
    #         tour_form = LYTourEnquiryForm()
    #         tour_form.full_name = full_name
    #         tour_form.email = email
    #         tour_form.contact = contact
    #         form_submission = LYTourEnquiry.objects.create(
    #             full_name=tour_form.full_name,
    #             email=tour_form.email,
    #             contact=tour_form.contact,
    #         )
    #         form_submission.save()
    #
    #         # Sending Email
    #         mail_subject = full_name + ' Enrolled for LY Tour '
    #         message = 'New Enrollment'
    #         message_content = {
    #             'full_name': full_name,
    #             'email': email,
    #             'contact': contact,
    #         }
    #         from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
    #         to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
    #         html_content = render_to_string('front/email/ly_tour_email.html', message_content)
    #         if full_name and email and contact:
    #             try:
    #                 send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
    #                 messages.success(request, 'Thank you for your enrollment. We have successfully booked your spot.')
    #                 return redirect('jaipur-tour')
    #             except BadHeaderError:
    #                 return HttpResponse('Invalid header found.')
    #         else:
    #             return HttpResponse('Make sure all fields are entered and valid.')
    #
    #     else:
    #         messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    #         return redirect('jaipur-tour')
    #
    # context = {
    #     'site_key': site_key,
    # }
    return render(request, 'front/pages/tour/jaipur-tour.html')


def tnvTour(request):
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']

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
            # Contact Form submission
            tour_form = LYTourEnquiryForm()
            tour_form.full_name = full_name
            tour_form.email = email
            tour_form.contact = contact
            form_submission = LYTourEnquiry.objects.create(
                full_name=tour_form.full_name,
                email=tour_form.email,
                contact=tour_form.contact,
                category='Thane-Navi-Mumbai',
            )
            form_submission.save()

            # Sending Email
            mail_subject = full_name + ' Enrolled for Thane & Navi Mumbai Tour '
            message = 'New Enrollment'
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/thane-navi-mumbai-email.html', message_content)
            if full_name and email and contact:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                    messages.success(request, 'Thank you for your enrollment. We have successfully booked your spot.')
                    return redirect('tnm-tour-ty')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('tnm-tour')

    context = {
        'site_key': site_key,
    }
    return render(request, 'front/pages/tour/thane-navi-mumbai-tour.html', context)


def tnvTourTY(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('tnm-tour')
    context = {}
    return render(request, 'front/pages/success/thane-navi-mumbai-thankyou.html', context)


def holidays(request):
    return render(request, 'front/pages/ly-holidays.html')


def LeaderTrainingCourse(request):
    all_countries = Country.objects.all()
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Contact Form submission
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Leader Training',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Leader Training Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('leader-training')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('leader-training')

    context = {
        'all_countries': all_countries,
        'stripe_public_key': stripe_public_key,
        'site_key': site_key,
    }
    return render(request, 'front/pages/leader-training.html', context)


def skypeLaughterClub(request):
    return render(request, 'front/pages/skype-laughter-club.html')


def zoomLaughterClub(request):
    site_key = WebSettings.public_key
    all_countries = Country.objects.all()

    if request.method == 'POST':
        country_data = request.POST['country_data']
        if country_data:
            country_code, country_name = country_data.split('|', 1)
        data = {
            'full_name': request.POST['name'],
            'email': request.POST['email'],
            'contact': request.POST['contact'],
            'occupation': request.POST['occupation'],
            'country': country_name,
            'token': secrets.token_urlsafe(16)
        }
        if not validate_recaptcha(request.POST.get('g-recaptcha-response')):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('zoom-laughter-club')

        save_form_data(data)

        # 👉🏻 Send Email
        if not send_zoom_lc_email(data):
            messages.error(request, 'Error sending the email.')
            return redirect('zlc-success')

        # 👉🏻 Send Whatsapp Notification
        if not send_whatsapp_notification(country_code, data['contact']):
            messages.error(request, 'Error sending the WhatsApp notification')
            return redirect('zlc-success')

        messages.success(request, 'Successfully signed up for Zoom Laughter Club.')
        return redirect('zlc-success')

    context = {
        'site_key': site_key,
        'all_countries': all_countries,
    }
    return render(request, 'front/pages/zoom-laughter-club.html', context)


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


def save_form_data(data):
    form_submission = ZoomLCEnquiry.objects.create(**data)
    form_submission.save()


def send_whatsapp_notification(country_code, contact):
    try:
        # 👉🏻 Sending WhatsApp Message
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        to_whatsapp_number = f'whatsapp:+{country_code}{contact}'

        titleTimeET = ' Eastern Time 10 pm WA Group:'
        whatsAppLinkET = 'https://chat.whatsapp.com/EFkidSrVNFgEyVyCYruX8v'

        titleTimeEU = ' Central Europe Time 1:30 pm WA Group:'
        whatsAppLinkEU = 'https://chat.whatsapp.com/JUDZdlmvBNK2UHaasA1haP'


        zlc_contentVariables = {
            '1': str(titleTimeET),
            '2': str(whatsAppLinkET),
            '3': str(titleTimeEU),
            '4': str(whatsAppLinkEU)
        }

        client.messages.create(
            content_sid='HXc66a3d69af1137f75344b09aa8f665fb',
            content_variables=json.dumps(zlc_contentVariables),
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


def send_zoom_lc_email(data):
    try:
        mail_subject = f"{data['full_name']} signed up for Zoom Laughter Club."
        message = 'New Enquiry Submitted'
        from_email = f"Laughter Yoga International <{settings.DEFAULT_FROM_EMAIL}>"
        to_email = (data['email'], 'Laughter Yoga International <help@laughteryoga.org>')
        html_content = render_to_string('front/email/zoom_lc_email.html', data)
        send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
        return True
    except BadHeaderError:
        return False
    except Exception as e:
        # Ideally, log the exception for debugging
        print(f"Error sending email: {e}")
        return False


def zlcSuccess(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('zoom-laughter-club')
    context = {}
    return render(request, 'front/pages/success/zoom-lc-thankyou.html', context)


def zlcNew(request):
    return render(request, 'front/pages/zlcNew.html')


def find_lyprofs(request):
    # Start with users who have an active subscription
    all_users = User.objects.filter(
        subscription__status='Active',  # Active subscriptions
        is_active=True,  # Account is active
        is_deleted=False  # Account is not soft-deleted
    ).distinct().order_by('first_name')

    # Fetch filters from GET request
    user_type = request.GET.get('user_type')
    country = request.GET.get('country')
    state = request.GET.get('state')
    city = request.GET.get('city')

    # Apply filters if provided
    if user_type:
        all_users = all_users.filter(UserProfile__user_type=user_type)
    if country:
        all_users = all_users.filter(UserAddress__country=country)
    if state:
        all_users = all_users.filter(UserAddress__state=state)
    if city:
        all_users = all_users.filter(UserAddress__city=city)

    # Set up pagination
    paginator = Paginator(all_users, 40)  # Adjust number per page as needed
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    data = {
        'all_users': paged_users,
        'form': UserForm,
    }
    return render(request, 'front/pages/member-list.html', data)


MEMBERSHIP_CARD_DIR = settings.BASE_DIR / 'media' / 'membership-cards'


def memberdetailsview(request, pk):
    user_detail = get_object_or_404(User, id=pk)
    JPG_FILE = MEMBERSHIP_CARD_DIR / f"membership-card-{pk}.jpg"
    file_exists = exists(JPG_FILE)  # To check the file is present on server or not
    lc_user = Club.objects.filter(author=user_detail).order_by('-created_date')
    user_detail.views = user_detail.views + 1
    user_detail.save()
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Contact Form submission
            tpe_form = ContactForm()
            tpe_form.full_name = full_name
            tpe_form.email = email
            tpe_form.contact = contact
            tpe_form.country = country
            tpe_form.message = message
            form_submission = TrainerProfileEnquiry.objects.create(
                full_name=tpe_form.full_name,
                email=tpe_form.email,
                contact=tpe_form.contact,
                country=tpe_form.country,
                message=tpe_form.message,
            )
            form_submission.save()

            # Sending Email to Trainer
            mail_subject = 'New Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            trainer_email = user_detail.email  # Fetching User Email to send email.
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (trainer_email,)
            html_content = render_to_string('front/email/masked-email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return HttpResponseRedirect(reverse('members-detail', args=(user_detail.id,)))
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return HttpResponseRedirect(reverse('members-detail', args=(user_detail.id,)))
    data = {
        'file_exists': file_exists,
        'user_detail': user_detail,
        'lc_user': lc_user,
        'site_key': site_key,
    }
    return render(request, 'front/pages/member-detail.html', data)


def verifiedRegisteredUsers(request):
    all_registered_user = User.objects.all().order_by('country')
    myFilteredMembers = RegisteredProfessionals(request.GET, queryset=all_registered_user)
    filtered_user = myFilteredMembers.qs
    paginator = Paginator(filtered_user, 200)
    page = request.GET.get('page')
    paged_filtered_user = paginator.get_page(page)
    data = {
        'all_registered_user': all_registered_user,
        'myFilteredMembers': myFilteredMembers,
        'filtered_user': paged_filtered_user,
    }
    return render(request, 'front/pages/registered-laughter-yoga-professionals.html', data)


def FinderTrainingView(request):
    all_trainings = Training.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    if request.GET.get('category_title'):
        # print(request.GET)
        state = request.GET.get('state', None)
        city = request.GET.get('city', None)
        country = request.GET.get('country', None)
        cat_title = request.GET.get('category_title')
        if city:
            all_trainings = Training.objects.filter(category_title__id=cat_title, country__id=country, state__id=state, city__id=city, start_date__gte=timezone.now()).order_by('start_date')
        elif state:
            all_trainings = Training.objects.filter(category_title__id=cat_title, country__id=country, state__id=state, start_date__gte=timezone.now()).order_by('start_date')
        elif country:
            all_trainings = Training.objects.filter(category_title__id=cat_title, country__id=country, start_date__gte=timezone.now()).order_by('start_date')
        else:
            all_trainings = Training.objects.filter(category_title__id=request.GET.get('category_title'), start_date__gte=timezone.now()).order_by('start_date')

    paginator = Paginator(all_trainings, 40)
    page = request.GET.get('page')
    paged_all_trainings = paginator.get_page(page)
    data = {
        'all_trainings': paged_all_trainings,
         'form': UserForm
    }
    return render(request, 'front/training/find-trainings-worldwide.html', data)


def FinderEventView(request):
    all_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    if request.GET.get('category'):
        print(request.GET)
        state = request.GET.get('state' ,None)
        city = request.GET.get('city' , None)
        country = request.GET.get('country' , None)
        cat_title = request.GET.get('category')

        if city:
            all_events = Event.objects.filter(category=cat_title, country__id=country, state__id=state, city__id=city, start_date__gte=timezone.now()).order_by('start_date')

        elif state:
            all_events = Event.objects.filter(category=cat_title, country__id=country, state__id=state, start_date__gte=timezone.now()).order_by('start_date')

        elif country:
            all_events = Event.objects.filter(category=cat_title, country__id=country, start_date__gte=timezone.now()).order_by('start_date')

        else:
            all_events = Event.objects.filter(category=request.GET.get('category'), start_date__gte=timezone.now()).order_by('start_date')

    #myEventFilter = EventFilter(request.GET, queryset=all_events)
    #all_events = myEventFilter.qs
    paginator = Paginator(all_events, 40)
    page = request.GET.get('page')
    paged_all_events = paginator.get_page(page)
    event_cat_filter = Event.objects.values_list('category', flat=True).distinct()
    event_country_filter = Event.objects.values_list('country__name', flat=True).distinct()
    event_state_filter = Event.objects.values_list('state__name', flat=True).distinct()
    event_city_filter = Event.objects.values_list('city__name', flat=True).distinct()
    data = {
        'all_events': paged_all_events,
#        'myEventFilter': myEventFilter,
        'event_cat_filter': event_cat_filter,
        'event_country_filter': event_country_filter,
        'event_state_filter': event_state_filter,
        'event_city_filter': event_city_filter,
        'form':EventFinderForm
    }
    return render(request, 'front/event/find-events-worldwide.html', data)


def FinderClubView(request):
    all_clubs = Club.objects.all().order_by('created_date')
    # myClubFilter = ClubFilter(request.GET, queryset=all_clubs)
    if request.GET.get('category_title'):
        print(request.GET)
        state = request.GET.get('state', None)
        city = request.GET.get('city', None)
        country = request.GET.get('country', None)
        cat_title = request.GET.get('category_title')
        if city:
            all_clubs = Club.objects.filter(
                category_title__id=cat_title, country=country, state=state, city=city
            )
        elif state:
            all_clubs = Club.objects.filter(
                category_title__id=cat_title, country=country, state=state
            )

        elif country:
            all_clubs = Club.objects.filter(
                category_title__id=cat_title, country=country
            )

            print(request.GET.get('country'))
        else:
            all_clubs = Club.objects.filter(
                category_title__id=request.GET.get('category_title'))
    # all_clubs = myClubFilter.qs
    paginator = Paginator(all_clubs, 40)
    page = request.GET.get('page')
    paged_all_trainings = paginator.get_page(page)
    data = {
        'all_clubs': paged_all_trainings,
        #   'myClubFilter': myClubFilter,
        "form": ClubFinderForm()
    }
    return render(request, 'front/club/find-clubs-worldwide.html', data)


def FinderwldView(request):
    return render(request, 'front/pages/find-world-laughter-day.html')


def ly2Landing(request):
    site_key = WebSettings.public_key
    all_countries = Country.objects.all()
    stripe_public_key = StripeGateway.public_key
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Create a LY2 Transaction
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='LY2',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New LY 2.0 Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('ly2')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('ly2')

    context = {
        'site_key': site_key,
        'all_countries': all_countries,
        'stripe_public_key': stripe_public_key,
    }

    return render(request, 'front/ly2/landing-page.html', context)


def ly2jpLanding(request):
    return render(request, 'front/ly2/jp/landing-page.html')


def DiaryListView(request):
    all_diaries = Diary.objects.all().order_by('-created_date')
    paginator = Paginator(all_diaries, 25)
    page = request.GET.get('page')
    paged_dairies = paginator.get_page(page)
    data = {
        'all_diaries': paged_dairies,
    }
    return render(request, 'front/diary/diary-list.html', data)


def DiaryDetailView(request, slug):
    single_diary = get_object_or_404(Diary, slug=slug)
    single_diary.views = single_diary.views + 1
    single_diary.save()
    data = {
        'single_diary': single_diary,
    }
    return render(request, 'front/diary/diary-detail.html', data)


# def LYArticlesListView(request):
#     all_ly_articles = LYArticles.objects.all().order_by('created_date')
#     paginator = Paginator(all_ly_articles, 25)
#     page = request.GET.get('page')
#     paged_ly_articles = paginator.get_page(page)
#     data = {
#         'all_ly_articles': paged_ly_articles,
#     }
#     return render(request, 'front/lyarticle/ly-articles-list.html', data)
#
#
# def LYArticlesDetailView(request, slug):
#     single_ly_article = get_object_or_404(LYArticles, slug=slug)
#     single_ly_article.views = single_ly_article.views + 1
#     single_ly_article.save()
#     data = {
#         'single_ly_article': single_ly_article,
#     }
#     return render(request, 'front/lyarticle/ly-articles-detail.html', data)


# ajax class

def load_countries(request):
    user_type = request.GET.get('id_user_type')
    # Fetching countries based on user profiles linked to accounts with addresses
    countries = Address.objects.filter(user__UserProfile__user_type=user_type) \
        .values('country__name', 'country__id').distinct().order_by('country__name')
    context = {'countries': [{'id': country['country__id'], 'name': country['country__name']} for country in countries]}
    html = render_to_string('front/ajax/country-dropdown.html', context, request=request)
    return JsonResponse({'html': html})


def load_states(request):
    id_country = request.GET.get('id_country')
    print("Received country ID:", id_country)  # Debugging output
    if not id_country:
        return JsonResponse({'html': '<option value="">Select State</option>'})  # Provide a fallback option

    states = State.objects.filter(country_id=id_country).values('id', 'name').order_by('name')
    print("Filtered states:", states)  # Debugging output
    html = render_to_string('front/ajax/state-dropdown.html', {'states': states})
    return JsonResponse({'html': html})


def load_cities(request):
    id_state = request.GET.get('id_state')
    if not id_state:
        return JsonResponse({'html': '<option value="">Select City</option>'})

    cities = City.objects.filter(state_id=id_state).values('id', 'name').order_by('name')
    html = render_to_string('front/ajax/city-dropdown.html', {'cities': cities})
    return JsonResponse({'html': html})


def comingSoon(request):
    return render(request, 'front/coming-soon.html')


def contactUs(request):
    site_key = WebSettings.public_key
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        country = request.POST['country']
        message = request.POST['message']

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
            # Contact Form submission
            contact_form = ContactForm()
            contact_form.full_name = full_name
            contact_form.email = email
            contact_form.contact = contact
            contact_form.country = country
            contact_form.message = message
            form_submission = Contact.objects.create(
                category='Contact',
                full_name=contact_form.full_name,
                email=contact_form.email,
                contact=contact_form.contact,
                country=contact_form.country,
                message=contact_form.message,
            )
            form_submission.save()

            # Sending Email
            mail_subject = 'New Enquiry Received from ' + full_name
            message_content = {
                'full_name': full_name,
                'email': email,
                'contact': contact,
                'country': country,
                'message': message,
            }
            from_email = 'Laughter Yoga International <settings.DEFAULT_FROM_EMAIL>'
            to_email = (email, 'Laughter Yoga International <help@laughteryoga.org>')
            html_content = render_to_string('front/email/enquiry_email.html', message_content)
            if full_name and email and contact and country and message:
                try:
                    send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Thank you. We have received your enquiry.')
                return redirect('contact-us')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('contact-us')

    context = {
        'site_key': site_key,
    }

    return render(request, 'front/contact/contact.html', context)


def laughterBlogsList(request):
    all_blogs = laughterBlogs.objects.all().order_by('-created_date')
    paginator = Paginator(all_blogs, 20)
    page = request.GET.get('page')
    paged_all_downloads = paginator.get_page(page)
    data = {
        'all_blogs': paged_all_downloads,
    }
    return render(request, 'front/pages/blogs/laughter-blogs.html', data)


def laughterBlogsDetail(request, slug):
    blog_detail = get_object_or_404(laughterBlogs, slug=slug)
    blog_detail.views = blog_detail.views + 1
    blog_detail.save()
    data = {
        'blog_detail': blog_detail,
    }
    return render(request, 'front/pages/blogs/detailed-layout.html', data)


def laughterBlogCatList(request, cat_slug):
    single_cat_blog = laughterBlogs.objects.filter(category__slug=cat_slug).order_by('-created_date')
    paginator = Paginator(single_cat_blog, 20)
    page = request.GET.get('page')
    paged_all_downloads = paginator.get_page(page)

    data = {
        'single_cat_blog': paged_all_downloads,
    }
    return render(request, 'front/pages/blogs/cat-landing-page.html', data)


def researchArticleList(request):
    all_research_articles = generalResearch.objects.all().order_by('-created_date')
    paginator = Paginator(all_research_articles, 40)
    page = request.GET.get('page')
    paged_all_research_articles = paginator.get_page(page)
    context = {
        'all_research_articles': paged_all_research_articles,
    }
    return render(request, 'front/pages/research-article/ra-list.html', context)


def researchArticleDetail(request, slug):
    ra_detail = get_object_or_404(generalResearch, slug=slug)
    ra_detail.views = ra_detail.views + 1
    ra_detail.save()
    context = {
        'ra_detail': ra_detail,
    }
    return render(request, 'front/pages/research-article/ra-detailed.html', context)


def faq(request):
    context = {}
    return render(request, 'front/pages/faq.html', context)


def laughterQuotient(request):
    return render(request, 'front/pages/laughter-quotient.html')


def watchVideos(request):
    context = {}
    return render(request, 'front/pages/watch-videos.html', context)


def proNewsletter(request):
    return render(request, 'newsletter/prozone/index.html')


def termsAndConditions(request):
    return render(request, 'front/pages/terms-and-conditions.html')


def privacyPolicy(request):
    return render(request, 'front/pages/privacy-policy.html')


def worldConference(request):
    allCountry = Country.objects.all()
    site_key = settings.RECAPTCHA_PUBLIC_KEY

    context = {
        'site_key': site_key,
        'allCountry': allCountry,
    }

    return render(request, 'front/pages/world-conference.html', context)


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def clylNew(request):
    return render(request, 'front/pages/clylt.html')


def blcNew(request):
    return render(request, 'front/pages/blcNew.html')


def spiritualRetreat(request):
    site_key = WebSettings.public_key
    if request.method == 'POST':
        country_code = request.POST['country_code']
        data = {
            'month': 'March 2024',
            'name': request.POST['name'],
            'email': request.POST['email'],
            'whatsapp': request.POST['whatsapp'],
            'location': request.POST['location'],
            'info': request.POST['info'],
            'accommodation': request.POST['accommodation'],
            'comments': request.POST['comments'],
            'token': secrets.token_urlsafe(16)
        }
        if not validate_recaptcha(request.POST.get('g-recaptcha-response')):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('spiritualRetreat')
        # Saving Data to the Database
        save_spiritual_data(data)

        # 👉🏻 Send Email
        if not send_spiritual_email(data):
            messages.error(request, 'Error sending the email.')
            return redirect('spiritualRetreat')

        # 👉🏻 Send Whatsapp Notification
        if not send_spiritual_notification(data, country_code):
            messages.error(request, 'Error sending the WhatsApp notification')
            return redirect('spiritualRetreat')

        messages.success(request, 'Successfully enrolled for Mindfulness Retreat.')
        return redirect('srSuccess')

    context = {
        'site_key': site_key,
    }
    return render(request, 'front/pages/spiritual-retreat.html', context)

def save_spiritual_data(data):
    form_submission = SpiritualRetreat.objects.create(**data)
    form_submission.save()


def send_spiritual_email(data):
    try:
        mail_subject = f"{data['name']} signed up for Laughter Yoga Mindfulness Retreat."
        message = 'New Enquiry Submitted'
        from_email = f"Laughter Yoga International <{settings.DEFAULT_FROM_EMAIL}>"
        to_email = (data['email'], 'Laughter Yoga International <help@laughteryoga.org>')
        html_content = render_to_string('front/email/spiritual-retreat-email.html', data)
        send_mail(mail_subject, message, from_email, to_email, html_message=html_content)
        # Update the whatsapp_status field on successful message send
        retreat = SpiritualRetreat.objects.get(token=data['token'])
        retreat.email_status = True
        retreat.save()
        return True
    except BadHeaderError:
        return False
    except Exception as e:
        # Ideally, log the exception for debugging
        print(f"Error sending email: {e}")
        return False

def send_spiritual_notification(data, country_code):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        to_whatsapp_number = f"whatsapp:{country_code}{data['whatsapp']}"

        name = data['name']
        accommodation = data['accommodation']

        content_variables = {
            '1': str(name),
            '2': str(accommodation),
        }
        client.messages.create(
            content_sid='HX07a5d03086958f0e96502f932e9dd1ad',
            content_variables=json.dumps(content_variables),
            from_='MG0485ae03bc7fb111cb65a6bd21b10938',
            to=to_whatsapp_number,
        )
        # Update the whatsapp_status field on successful message send
        retreat = SpiritualRetreat.objects.get(token=data['token'])
        retreat.whatsapp_status = True
        retreat.save()
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

def srSuccess(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect('spiritualRetreat')
    context = {}
    return render(request, 'front/pages/success/sr-thankyou.html', context)


def srPayment(request):
    context = {}
    return render(request, 'front/pages/payment/retreat-donation.html', context)


def timeZone(request):
    context = {}
    return render(request, 'front/pages/local-time.html', context)


def diaryList(request):
    all_diary_articles = Diary.objects.all().order_by('-created_date')
    paginator = Paginator(all_diary_articles, 40)
    page = request.GET.get('page')
    paged_all_diary_articles = paginator.get_page(page)
    data = {
        'all_diary_articles': paged_all_diary_articles,
    }
    return render(request, 'fe/pages/diary/list-layout.html', data)


def diarydetail(request, slug):
    diary_detail = get_object_or_404(Diary, slug=slug)
    diary_detail.views = diary_detail.views + 1
    diary_detail.save()
    data = {
        'diary_detail': diary_detail,
    }
    return render(request, 'fe/pages/diary/detailed-layout.html', data)


@superuser_required
def getInvolvedListView(request):
    allGILists = GetInvolved.objects.all().order_by("-created_date")
    pdSearch = request.GET.get('search', '').strip()
    if pdSearch:
        allGILists = allGILists.filter(
            Q(title__icontains=pdSearch)  # Ensure 'title' is a valid field name in your Diary model
        )
    paginator = Paginator(allGILists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_diary = paginator.get_page(page_number)
    context = {
        'allGILists': paged_pro_diary,
    }
    return render(request, 'be/apps/pages/getInvolved/read.html', context)


@superuser_required
def getInvolvedAddView(request):
    if request.method == 'POST':
        giForm = GetInvolvedForm(request.POST, request.FILES)
        if giForm.is_valid():
            gi = giForm.save(commit=False)
            gi.save()
            messages.success(request, 'Get Involved  published successfully!')
            return redirect('getInvolvedList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        giForm = GetInvolvedForm()

    context = {
        'giForm': giForm,
    }

    return render(request, 'be/apps/pages/getInvolved/create.html', context)


@superuser_required
def getInvolvedEditView(request, id):
    gi = get_object_or_404(GetInvolved, id=id)
    if request.method == 'POST':
        giForm = GetInvolvedForm(request.POST, request.FILES, instance=gi)
        if giForm.is_valid():
            giForm.save()
            messages.success(request, 'Get Involved updated successfully!')
            return redirect('getInvolvedList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        giForm = GetInvolvedForm(instance=gi)  # Populate the form with the existing diary data

    context = {
        'gi': gi,
        'giForm': giForm,
    }
    return render(request, 'be/apps/pages/getInvolved/update.html', context)


@superuser_required
def getInvolvedDeleteView(request, id):
    gi = get_object_or_404(GetInvolved, id=id)
    if request.method == 'POST':
        gi.delete()
        messages.success(request, 'Get Involved deleted successfully!')
        return redirect('getInvolvedList')

    context = {
        'gi': gi,
    }
    return render(request, 'be/apps/pages/getInvolved/delete.html', context)


@superuser_required
def DiaryListView(request):
    allPDLists = Diary.objects.all().order_by("-created_date")
    pdSearch = request.GET.get('search', '').strip()
    if pdSearch:
        allPDLists = allPDLists.filter(
            Q(title__icontains=pdSearch)  # Ensure 'title' is a valid field name in your Diary model
        )
    paginator = Paginator(allPDLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_diary = paginator.get_page(page_number)
    context = {
        'allPDLists': paged_pro_diary,
    }
    return render(request, 'be/apps/pages/diary/read.html', context)


@superuser_required
def DiaryAddView(request):
    if request.method == 'POST':
        pdForm = DiaryForm(request.POST, request.FILES)
        if pdForm.is_valid():
            d = pdForm.save(commit=False)
            d.save()
            messages.success(request, 'Diary published successfully!')
            return redirect('DiaryList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pdForm = DiaryForm()

    context = {
        'pdForm': pdForm,
    }

    return render(request, 'be/apps/pages/diary/create.html', context)


@superuser_required
def DiaryEditView(request, slug):
    diary = get_object_or_404(Diary, slug=slug)
    if request.method == 'POST':
        pdForm = DiaryForm(request.POST, request.FILES, instance=diary)
        if pdForm.is_valid():
            pdForm.save()
            messages.success(request, 'Diary updated successfully!')
            return redirect('DiaryList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pdForm = DiaryForm(instance=diary)  # Populate the form with the existing diary data

    context = {
        'diary': diary,
        'pdForm': pdForm,
    }
    return render(request, 'be/apps/pages/diary/update.html', context)


@superuser_required
def DiaryDeleteView(request, slug):
    diary = get_object_or_404(Diary, slug=slug)
    if request.method == 'POST':
        diary.delete()
        messages.success(request, 'Diary deleted successfully!')
        return redirect('DiaryList')

    context = {
        'diary': diary,
    }
    return render(request, 'be/apps/pages/diary/delete.html', context)


@superuser_required
def blogListView(request):
    allLBLists = laughterBlogs.objects.all().order_by("-created_date")
    ppSearch = request.GET.get('search', '').strip()
    if ppSearch:
        allLBLists = allLBLists.filter(
            Q(title__icontains=ppSearch)
        )
    paginator = Paginator(allLBLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_blogs = paginator.get_page(page_number)
    context = {
        'allLBLists': paged_blogs,
    }
    return render(request, 'be/apps/pages/blog/read.html', context)


@superuser_required
def blogAddView(request):
    if request.method == 'POST':
        bForm = BlogsForm(request.POST, request.FILES)
        if bForm.is_valid():
            blog = bForm.save(commit=False)
            blog.save()
            messages.success(request, 'Blog published successfully!')
            return redirect('blogList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        bForm = BlogsForm()

    context = {
        'bForm': bForm,
    }

    return render(request, 'be/apps/pages/blog/create.html', context)


@superuser_required
def blogEditView(request, slug):
    blog = get_object_or_404(laughterBlogs, slug=slug)
    if request.method == 'POST':
        bForm = BlogsForm(request.POST, request.FILES, instance=blog)
        if bForm.is_valid():
            bForm.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('blogList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        bForm = BlogsForm(instance=blog)  # Populate the form with the existing diary data

    context = {
        'blog': blog,
        'bForm': bForm,
    }
    return render(request, 'be/apps/pages/blog/update.html', context)


@superuser_required
def blogDeleteView(request, slug):
    blog = get_object_or_404(laughterBlogs, slug=slug)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('blogList')

    context = {
        'blog': blog,
    }
    return render(request, 'be/apps/pages/blog/delete.html', context)


def graList(request):
    all_research_articles = generalResearch.objects.all().order_by('-created_date')
    paginator = Paginator(all_research_articles, 40)
    page = request.GET.get('page')
    paged_all_research_articles = paginator.get_page(page)
    data = {
        'all_research_articles': paged_all_research_articles,
    }
    return render(request, 'fe/pages/research-articles/list-layout.html', data)


def gradetail(request, slug):
    research_detail = get_object_or_404(generalResearch, slug=slug)
    research_detail.views = research_detail.views + 1
    research_detail.save()
    data = {
        'research_detail': research_detail,
    }
    return render(request, 'fe/pages/research-articles/detailed-layout.html', data)


def graListView(request):
    allGRALists = generalResearch.objects.all().order_by("-created_date")
    graSearch = request.GET.get('search', '').strip()
    if graSearch:
        allGRALists = allGRALists.filter(
            Q(title__icontains=graSearch)  # Ensure 'title' is a valid field name in your ProResearch model
        )
    paginator = Paginator(allGRALists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_general_ra = paginator.get_page(page_number)
    context = {
        'allGRALists': paged_general_ra,
    }
    return render(request, 'be/apps/pages/research/read.html', context)


@superuser_required
def graAddView(request):
    if request.method == 'POST':
        graForm = gResearchForm(request.POST, request.FILES)
        if graForm.is_valid():
            gRA = graForm.save(commit=False)
            gRA.save()
            messages.success(request, 'Research Article published successfully!')
            return redirect('graList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        graForm = gResearchForm()

    context = {
        'graForm': graForm,
    }

    return render(request, 'be/apps/pages/research/create.html', context)


@superuser_required
def graEditView(request, slug):
    generalRA = get_object_or_404(generalResearch, slug=slug)
    if request.method == 'POST':
        graForm = gResearchForm(request.POST, request.FILES, instance=generalRA)
        if graForm.is_valid():
            graForm.save()
            messages.success(request, 'Research Article updated successfully!')
            return redirect('graList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        graForm = gResearchForm(instance=generalRA)  # Populate the form with the existing diary data

    context = {
        'generalRA': generalRA,
        'graForm': graForm,
    }
    return render(request, 'be/apps/pages/research/update.html', context)


@superuser_required
def graDeleteView(request, slug):
    generalRA = get_object_or_404(generalResearch, slug=slug)
    if request.method == 'POST':
        generalRA.delete()
        messages.success(request, 'Research Article deleted successfully!')
        return redirect('raList')

    context = {
        'generalRA': generalRA,
    }
    return render(request, 'be/apps/pages/research/delete.html', context)


@require_POST
@login_required
@csrf_exempt
def addBlogCategory(request):
    name = request.POST.get('name')
    if name:
        category, created = laughterBlogsCat.objects.get_or_create(title=name)
        return JsonResponse({'success': True, 'category_id': category.id})
    return JsonResponse({'success': False})


def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('name')
    context = {
        'states': states,
    }
    return render(request, 'be/apps/settings/stateDropdownList.html', context)


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    context = {
        'cities': cities,
    }
    return render(request, 'be/apps/settings/cityDropdownList.html', context)


def load_authors(request):
    if 'author_name' in request.GET:
        author_name = request.GET.get('author_name')
        # Fetch a limited number of authors based on the search query
        authors = User.objects.filter(email__icontains=author_name)[:10]
        author_data = [{'id': author.id, 'text': author.email} for author in authors]
        return JsonResponse({'results': author_data})
    else:
        return JsonResponse({}, status=400)