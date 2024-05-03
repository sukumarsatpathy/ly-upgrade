from django.contrib import sitemaps
from django.urls import reverse

from club.models import Club
from event.models import Event
from training.models import Training
from news.models import News
from testimonial.models import Testimonial


class StaticPageSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about-laughter-yoga', 'school-children', 'business', 'seniors', 'depression', 'special-needs',
                'cancer', 'yoga-plus-ly', 'laughter-yoga-research', 'basic-learning-course', 'mental-health',
                'leader-training', 'zoom-laughter-club', 'about-training', 'teacher-training', 'find-ly-professionals',
                'find-registered-laughter-yoga-professionals', 'find-training', 'find-event', 'find-club', 'find-wld',
                'prozone', 'ly2', 'ly2jp', 'diary-list', 'news', 'testimonial', 'world-laughter-day',
                'wld-message-from-drk', 'wld-round-logo', 'wld-blue-bg-logo', 'wld-banner', 'terms-and conditions',
                'privacy-policy', 'faq', 'contact-us', 'login', 'forgotPassword']

    def location(self, item):
        return reverse(item)

class TrainingSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Training.objects.all()

    def lastmod(self, obj):
        return obj.modified_date


class EventSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.modified_date


class ClubSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Club.objects.all()

    def lastmod(self, obj):
        return obj.modified_date