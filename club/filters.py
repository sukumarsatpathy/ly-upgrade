import django_filters
from .models import Club
from django_filters import CharFilter, BooleanFilter, ChoiceFilter
from django.utils.translation import gettext_lazy as _


class ClubFilter(django_filters.FilterSet):
    category_title = CharFilter(label=_('Club Category'), field_name='category_title__title', lookup_expr='icontains')
    country = CharFilter(label=_('Country'), field_name='country__name', lookup_expr='icontains')
    state = CharFilter(label=_('State'), field_name='state__name', lookup_expr='icontains')
    city = CharFilter(label=_('City'), field_name='city__name', lookup_expr='icontains')
    #author = CharFilter(label=_('Trainer Name'), field_name='trainer_name', lookup_expr='icontains')

    class Meta:
        model = Club
        fields = ['category_title', 'country', 'state', 'city']