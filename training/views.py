from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Training
from .forms import AddTrainingForm, EditTrainingForm , UserForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from core.decorators import is_auth_or_superuser_edit_view, user_has_active_membership

from .models import Training
from .forms import TrainingForm


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


def TrainingDetailsView(request, pk):
    training_detail = get_object_or_404(Training, pk=pk)
    training_detail.views = training_detail.views + 1
    training_detail.save()
    data = {
        'training_detail': training_detail,
    }
    return render(request, 'front/training/training-detail.html', data)


class AddTrainingView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = AddTrainingForm
    template_name = 'front/training/add-training.html'


class EditTrainingView(LoginRequiredMixin, UpdateView):
    model = Training
    form_class = EditTrainingForm
    template_name = 'front/training/edit-training.html'


class DeleteTrainingView(LoginRequiredMixin, DeleteView):
    model = Training
    template_name = 'front/training/delete-training.html'
    success_url = reverse_lazy('list-training')


class ListTrainingView(LoginRequiredMixin, ListView):
    model = Training
    template_name = 'front/training/list-training.html'
    ordering = '-start_date'


def load_countries(request):
    countries_list = []
    category_type = request.GET.get('id_category')
    # print("CATEGORY:",category_type)
    categories_obj = Training.objects.filter(category_title=category_type).values('country__name' , 'country__id').distinct().exclude(country__name=None).order_by('country__name')
    # print("Category Object:",categories_obj)
    for category in categories_obj:
        country_dict = {}
        country_dict['country'] = category.get('country__name')
        country_dict['id'] = category.get('country__id')
        countries_list.append(country_dict)
    return render(request, 'country_dropdown_list_options.html', {'countries': countries_list})


def load_state(request):
    # print("state")
    states_list = []
    category_type = request.GET.get('id_category')
    id_country = request.GET.get('id_country')
    # print(request.GET)
    categories_obj = Training.objects.filter(category_title=category_type , country =id_country  ).values('state__name' , 'state__id').distinct().exclude(state__name=None)
    # print(categories_obj)
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
    # print(request.GET)
    categories_obj = Training.objects.filter(category_title=category_type, country=id_country, state=id_state).values('city__name', 'city__id').distinct().exclude(city__name=None)
    # print(categories_obj)
    for category in categories_obj:
        city_dict = {}
        city_dict['city'] = category.get('city__name')
        city_dict['id'] = category.get('city__id')
        cites_list.append(city_dict) 
    # print(cites_list)
    return render(request, 'city_dropdown.html', {'cites': cites_list})



def filter_trainings(trainings_queryset, filter_value):
    # Define a subquery for active memberships
    now = timezone.now()
    active_memberships = Subscription.objects.filter(
        user=OuterRef('author'), status="Published", endDate__gte=now
    )

    # Filter trainings based on the filter_value
    if filter_value == 'virtual':
        trainings_queryset = trainings_queryset.filter(type='Virtual Training')
    elif filter_value == 'physical':
        trainings_queryset = trainings_queryset.filter(type='Physical Training')

    # Annotate trainings queryset with active subscription status
    trainings_queryset = trainings_queryset.annotate(
        has_active_membership=Exists(active_memberships)
    )

    return trainings_queryset.order_by('-created_date')


@login_required(login_url='login')
def trainingListView(request):
    currentUser = request.user
    now = timezone.now()

    # Show all trainings to superusers, otherwise show user-specific trainings
    if currentUser.is_superuser:
        trainingsQuerySet = Training.objects.all()
    else:
        # This is an example, adjust the filter based on your model relationships and requirements
        trainingsQuerySet = Training.objects.filter(author=currentUser)

    filter_value = request.POST.get('filterSelect')

    # Apply filtering if filter value is provided
    if filter_value and filter_value != 'all':
        trainingsQuerySet = filter_trainings(trainingsQuerySet, filter_value)

    # Handle search functionality
    tSearch = request.GET.get('trainingSearch','').strip()
    if tSearch:
        trainingsQuerySet = trainingsQuerySet.filter(
            Q(category__icontains=tSearch) |
            Q(type__icontains=tSearch) |
            Q(title__icontains=tSearch) |
            Q(author__first_name__icontains=tSearch) |
            Q(author__last_name__icontains=tSearch) |
            Q(trainingcontact__trainer__icontains=tSearch)
        )

    # Define a subquery for active memberships
    active_memberships = Subscription.objects.filter(
        user=OuterRef('author'), status='Active', endDate__gte=now
    )

    # Annotate trainings queryset with active subscription status
    trainingsQuerySet = trainingsQuerySet.annotate(
        has_active_membership=Exists(active_memberships)
    )

    # Reverse the ordering to show latest trainings first
    trainingsQuerySet = trainingsQuerySet.order_by('-created_date')

    # Handle pagination
    items_per_page = int(request.GET.get('items', 10))  # Defaulted to 10
    paginator = Paginator(trainingsQuerySet, items_per_page)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_trainings = paginator.get_page(page_number)

    context = {
        'allTrainings': paged_trainings,
        'items_per_page': items_per_page,
        'filter_value': filter_value,
    }
    return render(request, 'be/apps/training/read.html', context)



@user_has_active_membership
def trainingAddView(request, pk=None):
    now = timezone.now()

    if request.method == 'POST':
        tForm = TrainingForm(request.POST, user=request.user)
        taForm = TrainingAddressForm(request.POST)
        tcForm = TrainingContactForm(request.POST, user=request.user)
        tdForm = TrainingDatesForm(request.POST)
        tvForm = TrainingVideoForm(request.POST)
        tiForm = TrainingImagesForm(request.POST, request.FILES)

        forms_are_valid = all([
            tForm.is_valid(),
            taForm.is_valid(),
            tcForm.is_valid(),
            tdForm.is_valid(),
            tvForm.is_valid(),
            tiForm.is_valid()
        ])

        if forms_are_valid:
            # Save the main Training form first
            training_instance = tForm.save(commit=False)
            if not request.user.is_superuser:
                training_instance.author = request.user
            training_instance.save()

            # Associating and saving related forms with the training_instance
            for form in [taForm, tcForm, tdForm, tvForm]:
                instance = form.save(commit=False)
                instance.training = training_instance
                instance.save()

            # Handle the image form specially if an image is provided
            if 'image' in request.FILES:
                training_image = tiForm.save(commit=False)
                training_image.training = training_instance
                training_image.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Training added successfully.',
                    'redirect_url': reverse('trainingList')
                })
            else:
                messages.success(request, 'Training added successfully.')
                return redirect('trainingList')
        else:
            # Handle form errors
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Assuming tiForm to contain all relevant errors, customize as necessary
                return JsonResponse({'success': False, 'errors': tiForm.errors}, status=400)
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        # Initialize forms for a GET request
        tForm = TrainingForm(user=request.user)
        taForm = TrainingAddressForm()
        tcForm = TrainingContactForm(user=request.user)
        tdForm = TrainingDatesForm()
        tvForm = TrainingVideoForm()
        tiForm = TrainingImagesForm()

    context = {
        'tForm': tForm,
        'taForm': taForm,
        'tcForm': tcForm,
        'tdForm': tdForm,
        'tvForm': tvForm,
        'tiForm': tiForm
    }
    return render(request, 'be/apps/training/create.html', context)


@user_has_active_membership
@is_auth_or_superuser_edit_view(model=Training, redirect_url='dashboard')
def trainingEditView(request, pk):
    singleTraining = get_object_or_404(Training, id=pk)
    singleAddress = TrainingAddress.objects.filter(training=singleTraining).first()
    singleDate = TrainingDates.objects.filter(training=singleTraining).first()
    singleContact = TrainingContact.objects.filter(training=singleTraining).first()
    singleImage = TrainingImages.objects.filter(training=singleTraining).first()
    singleVideo = TrainingVideo.objects.filter(training=singleTraining).first()

    if request.method == 'POST':
        tForm = TrainingEditForm(request.POST, instance=singleTraining)
        taForm = TrainingAddressForm(request.POST, instance=singleAddress)
        tcForm = TrainingContactForm(request.POST, instance=singleContact)
        tdForm = TrainingDatesForm(request.POST, instance=singleDate)
        tvForm = TrainingVideoForm(request.POST, instance=singleVideo)
        tiForm = TrainingImagesForm(request.POST, request.FILES, instance=singleImage)

        if all([tForm.is_valid(), taForm.is_valid(), tcForm.is_valid(), tdForm.is_valid(), tvForm.is_valid(), tiForm.is_valid()]):
            tForm.save()
            taForm.save()
            tcForm.save()
            tdForm.save()
            tvForm.save()
            tiForm.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # For AJAX requests, respond with JSON including redirect URL
                return JsonResponse({
                    'success': True,
                    'message': 'Training added successfully.',
                    'redirect_url': reverse('trainingList')  # Provide the URL to redirect to
                })
            else:
                messages.success(request, 'Training added successfully.')
                return redirect('trainingList')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': tiForm.errors}, status=400)
            messages.error(request, 'Please correct the errors below.')
    else:
        tForm = TrainingEditForm(instance=singleTraining)
        taForm = TrainingAddressForm(instance=singleAddress)
        tcForm = TrainingContactForm(instance=singleContact)
        tdForm = TrainingDatesForm(instance=singleDate)
        tvForm = TrainingVideoForm(instance=singleVideo)
        tiForm = TrainingImagesForm(instance=singleImage)

    context = {
        'tForm': tForm,
        'taForm': taForm,
        'tcForm': tcForm,
        'tdForm': tdForm,
        'tvForm': tvForm,
        'tiForm': tiForm,
        'singleTraining': singleTraining  # Passing singleTraining for template use
    }
    return render(request, 'be/apps/training/update.html', context)


@login_required(login_url='login')
def trainingDeleteView(request, pk):
    currentUser = request.user
    training = get_object_or_404(Training, id=pk)
    if currentUser.is_superuser or currentUser.is_admin or currentUser == training.author:
        if request.method == "POST":
            training.delete()
            messages.success(request, 'You have successfully deleted the event!')
            return redirect('eventList')
    else:
        messages.error(request, 'You do not have permission to delete this event.')

    context = {
        'training': training,
    }
    return render(request, 'be/apps/training/delete.html', context)
    
