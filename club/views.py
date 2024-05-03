from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Club
from .forms import ClubForm,ClubFinderForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ClubFilter
from django.core.paginator import Paginator
from django.db.models import Q


class AddClubView(LoginRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'front/club/add-club.html'


class EditClubView(LoginRequiredMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'front/club/edit-club.html'


class DeleteClubView(LoginRequiredMixin, DeleteView):
    model = Club
    template_name = 'front/club/delete-club.html'
    success_url = reverse_lazy('list-club')


class ListClubView(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'front/club/list-club.html'
    ordering = '-created_date'


def FinderClubView(request):
    all_clubs = Club.objects.all().order_by('created_date')
    #myClubFilter = ClubFilter(request.GET, queryset=all_clubs)
    if request.GET.get('category_title'):
        print(request.GET)
        state = request.GET.get('state' ,None)
        city = request.GET.get('city' , None)
        country = request.GET.get('country' , None)
        cat_title = request.GET.get('category_title')
        if  city :
            all_clubs = Club.objects.filter( 
                category_title__id= cat_title ,  country=country , state=state   , city=city
            )
        elif  state:
            all_clubs = Club.objects.filter(
           category_title__id= cat_title ,  country=country , state=state 
            )

        elif  country   :
            all_clubs = Club.objects.filter(
            category_title__id= cat_title , country=country
            )
            
            print(request.GET.get('country'))
        else:
            all_clubs = Club.objects.filter(
            category_title__id=request.GET.get('category_title'))
    #all_clubs = myClubFilter.qs
    paginator = Paginator(all_clubs, 40)
    page = request.GET.get('page')
    paged_all_trainings = paginator.get_page(page)
    data = {
        'all_clubs': paged_all_trainings,
     #   'myClubFilter': myClubFilter,
       "form":ClubFinderForm()
    }
    return render(request, 'front/club/find-clubs-worldwide.html', data)


def ClubDetailsView(request, pk):
    club_detail = get_object_or_404(Club, pk=pk)
    club_detail.views = club_detail.views + 1
    club_detail.save()
    data = {
        'club_detail': club_detail,
    }
    return render(request, 'front/club/club-detail.html', data)



# ajax class


def load_countries(request):
    countries_list = []
    category_type = request.GET.get('id_category')
    print("CATEGORY:",category_type)
    categories_obj   = Club.objects.filter(category_title=category_type).values('country__name' , 'country__id').distinct().exclude(country__name=None).order_by('country__name')
    print("Category Object:",categories_obj)
    for category in categories_obj:
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


    categories_obj   = Club.objects.filter(category_title=category_type , country =id_country  ).values('state__name' , 'state__id').distinct().exclude(state__name=None)
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
    categories_obj    = Club.objects.filter(category_title=category_type , country=id_country  ,  state=id_state ).values('city__name' , 'city__id').distinct().exclude(city__name = None)
    print(categories_obj)
    for category in categories_obj:
        city_dict = {}
        city_dict['city'] = category.get('city__name')
        city_dict['id'] = category.get('city__id')
        cites_list.append(city_dict) 
    print(cites_list)
    return render(request, 'city_dropdown.html', {'cites': cites_list})

    
