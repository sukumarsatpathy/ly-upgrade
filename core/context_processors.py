import logging
from datetime import timedelta
from django.utils import timezone
from settings.models import WebSettings
from subscription.models import Subscription


logger = logging.getLogger(__name__)


#
def webSettingsUnivarsal(request):
    context = {
        'webSettingsUniversal': '',
    }
    try:
        webSettingsUniversal = WebSettings.objects.first()

        # Assuming all these fields are mandatory for the site's operation
        if not webSettingsUniversal:
            raise ValueError("No settings available in the WebsiteSettings table.")

        context['webSettingsUniversal'] = webSettingsUniversal

    # except webSettingsUniversal.DoesNotExist:
    #     # This block can be left empty or logged as it's essentially a silent fail and caught above
    #     logger.warning("WebsiteSettings does not exist. Using default settings.")
    #     return {'webSettingsUniversal': ''}

    except AttributeError as e:
        # Handle any attribute error and log it
        logger.error(f"An attribute error occurred: {e}. Using default settings for the missing attributes.")
        return {'webSettingsUniversal': ''}

    except ValueError as e:
        # Handle the custom exception raised above
        logger.error(f"ValueError: {e}. Using default settings.")
        return {'webSettingsUniversal': ''}

    except Exception as e:
        # This is a general exception handler. Use this sparingly and only for unexpected errors.
        logger.critical(f"Unexpected error occurred when fetching site settings: {e}. Using default settings.")
        return {'webSettingsUniversal': ''}

    return context


def active_membership(request):
    context = {
        'has_active_membership': False,
        'membership_expires_soon': False,
        'days_until_expiry': None,  # Initialize with None to indicate no expiry soon by default
    }

    if request.user.is_authenticated:
        now = timezone.now()
        expiry_threshold = now + timedelta(days=30)
        subscriptions = Subscription.objects.filter(
            user=request.user,
            status='Active',
            endDate__gte=now
        ).order_by('endDate')  # Order by expiry_date to get the closest expiry date first

        if subscriptions.exists():
            context['has_active_membership'] = True
            # Check if any of the active subscriptions expire within the next 30 days
            soon_to_expire_subscriptions = subscriptions.filter(endDate__lte=expiry_threshold)
            if soon_to_expire_subscriptions.exists():
                context['membership_expires_soon'] = True
                nearest_expiry_date = soon_to_expire_subscriptions.first().endDate
                days_until_expiry = (nearest_expiry_date - now).days
                context['days_until_expiry'] = days_until_expiry

    # The function will return the initial context if no active subscriptions are found,
    # effectively indicating that nothing related to memberships should be displayed.
    return context