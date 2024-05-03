from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Event
from .forms import AddEventForm, EditEventForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import EventFilter
from django.core.paginator import Paginator
from .forms  import EventFinderForm
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

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


def EventDetailsView(request, id):
    event_detail = get_object_or_404(Event, pk=id)
    event_detail.views = event_detail.views + 1
    event_detail.save()
    data = {
        'event_detail': event_detail,
    }
    return render(request, 'front/event/event-detail.html', data)


class AddEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = AddEventForm
    template_name = 'front/event/add-event.html'


class EditEventView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EditEventForm
    template_name = 'front/event/edit-event.html'


class DeleteEventView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'front/event/delete-event.html'
    success_url = reverse_lazy('list-event')


class ListEventView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'front/event/list-event.html'
    ordering = '-start_date'

# ajax class


def load_countries(request):
    countries_list = []
    category_type = request.GET.get('id_category')
    print("CATEGORY:",category_type)
    categories_obj   = Event.objects.filter(category=category_type).values('country__name' , 'country__id').distinct().exclude(country__name=None).order_by('country__name')
    print("Category Object:",categories_obj)
    for category in categories_obj:
        print(category)
        country_dict = {}
        country_dict['country'] = category.get('country__name')
        country_dict['id'] = category.get('country__id')
        countries_list.append(country_dict)
    return render(request, 'country_dropdown_list_options.html', {'countries': countries_list})


 




 

def load_state(request):
    print("state")
    states_list = []
    category_type = request.GET.get('id_category')
    id_country = request.GET.get('id_country')
    print(request.GET)


    categories_obj   = Event.objects.filter(category=category_type , country =id_country  ).values('state__name' , 'state__id').distinct().exclude(state__name=None)
    print(categories_obj)
    for category in categories_obj:
        state_dict = {}
        state_dict['states'] = category.get('state__name')
        state_dict['id'] = category.get('state__id')
        states_list.append(state_dict) 
    return render(request, 'state_dropdown.html', {'states': states_list})

 

def load_cites(request):
    cites_list = []
    category_type = request.GET.get('id_category')
    id_country = request.GET.get('id_country')
    id_state = request.GET.get('id_state')
    print(request.GET)
    categories_obj    = Event.objects.filter(category=category_type , country=id_country  ,  state=id_state ).values('city__name' , 'city__id').distinct().exclude(city__name = None)
    print(categories_obj)
    for category in categories_obj:
        city_dict = {}
        city_dict['city'] = category.get('city__name')
        city_dict['id'] = category.get('city__id')
        cites_list.append(city_dict) 
    print(cites_list)
    return render(request, 'city_dropdown.html', {'cites': cites_list})

 
