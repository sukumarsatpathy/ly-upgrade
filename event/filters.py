import django_filters
from .models import Event
from django_filters import CharFilter, BooleanFilter, ChoiceFilter
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from settings.models import Country, State, City


class EventFilter(django_filters.FilterSet):
    #category = django_filters.filters.ModelChoiceFilter(label=_('Event Category'), field_name='content_object__tags__name', to_field_name='category', queryset=Event.objects.all())
    #country = django_filters.filters.ModelChoiceFilter(label=_('Country'), field_name='country', to_field_name='name', queryset=Country.objects.all())
    #state = django_filters.filters.ModelChoiceFilter(label=_('State'), field_name='state__name', to_field_name='name', queryset=State.objects.all(), method='filter_by_country')
    #city = django_filters.filters.ModelChoiceFilter(label=_('City'), field_name='city__name', to_field_name='name', queryset=City.objects.all(), method='filter_by_state')

    category = CharFilter(label=_('Event Category'), field_name='category', lookup_expr='icontains')
    country = CharFilter(label=_('Country'), field_name='country__name', lookup_expr='icontains')
    state = CharFilter(label=_('State'), field_name='state__name', lookup_expr='icontains')
    city = CharFilter(label=_('City'), field_name='city__name', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['category', 'country', 'state', 'city']


    #def filter_by_country(self, queryset, name, value):
    #    expression = 'country' if value == 'ascending' else '-country'
    #    return queryset.order_by(expression)

    #def filter_by_state(self, queryset, name, value):
    #    expression = 'state' if value == 'ascending' else '-state'
    #    return queryset.order_by(expression)