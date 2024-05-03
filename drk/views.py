import logging
from django.shortcuts import render
from .models import UpcomingEvents
from collections import defaultdict
from django.utils import timezone

# Setup basic logging
logger = logging.getLogger(__name__)


def upcomingEvents(request):
    all_events = UpcomingEvents.objects.filter(is_active=True).order_by('startDate')
    grouped_events = defaultdict(list)

    for event in all_events:
        if event.startDate:
            # Ensure the datetime is timezone-aware
            event_date = event.startDate
            if timezone.is_naive(event_date):
                # Assuming the naive datetime is in the default timezone
                event_date = timezone.make_aware(event_date, timezone.get_default_timezone())

            # Format the date as needed
            month_year_key = event_date.strftime('%B %Y')
            grouped_events[month_year_key].append(event)

    context = {
        'grouped_events': dict(grouped_events)
    }
    return render(request, 'front/drk/landingpage.html', context)