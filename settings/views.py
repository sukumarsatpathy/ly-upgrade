from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Exists, OuterRef, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from core.decorators import superuser_required
from .models import WebSettings, MailServer, StripeGateway, RazorPayGateway, Country, State, City, Twilio, Services, Membership, Changelog
from .forms import WebSettingsForm, MailServerForm, StripeGatewayForm, RazorPayGatewayForm, CountryForm, StateForm, CityForm, TwilioForm, MembershipForm


@superuser_required
def webSettingsView(request):
    try:
        website_settings = WebSettings.objects.first()
    except WebSettings.DoesNotExist:
        messages.error(request, 'You are not authorised to view this page.')
        return redirect('dashboard')

    if request.method == 'POST':
        ws_form = WebSettingsForm(request.POST, request.FILES, instance=website_settings)
        if ws_form.is_valid():
            if ws_form.has_changed():
                ws_form.save()
                messages.success(request, 'Your settings have been updated.')
                return redirect('webSettings')
            else:
                messages.info(request, 'Nothing has changed.')
        else:
            messages.error(request, 'Form data is invalid. Please correct the errors.')
    else:
        ws_form = WebSettingsForm(instance=website_settings)

    context = {
        'website_settings': website_settings,
        'ws_form': ws_form,
    }
    return render(request, 'be/apps/settings/webSettingUpdate.html', context)


@superuser_required
def mailServerView(request):
    try:
        ms_settings = MailServer.objects.first()
    except MailServer.DoesNotExist:
        messages.error(request, 'You are not authorised to view this page.')
        return redirect('dashboard')

    if request.method == 'POST':
        ms_form = MailServerForm(request.POST, instance=ms_settings)
        if ms_form.is_valid():
            if ms_form.has_changed():
                ms_form.save()
                messages.success(request, 'Your mail server settings has been updated.')
                return redirect('mailServer')
            else:
                messages.info(request, 'Nothing has changed.')
    else:
        ms_form = MailServerForm(instance=ms_settings)

    context = {
        'ms_settings': ms_settings,
        'ms_form': ms_form,
    }
    return render(request, 'be/apps/settings/mailServerUpdate.html', context)


@superuser_required
def stripeGatewayView(request):
    spg_settings = StripeGateway.objects.first()

    if request.method == 'POST':
        # If settings exist, update the existing one
        if spg_settings:
            spg_form = StripeGatewayForm(request.POST, instance=spg_settings)
        # If no settings are available, create a new one
        else:
            spg_form = StripeGatewayForm(request.POST)

        if spg_form.is_valid():
            if not spg_settings or spg_form.has_changed():
                spg_form.save()
                if spg_settings:
                    messages.success(request, 'Your payment gateway settings have been updated.')
                else:
                    messages.success(request, 'Your payment gateway settings have been saved.')
                return redirect('stripeGatewayView')
            else:
                messages.info(request, 'Nothing has changed.')
        else:
            messages.error(request, 'There was an error in your form.')
    else:
        if spg_settings:
            spg_form = StripeGatewayForm(instance=spg_settings)
        else:
            spg_form = StripeGatewayForm()

    context = {
        'spg_settings': spg_settings,
        'spg_form': spg_form,
    }
    return render(request, 'be/apps/settings/stripeGatewayUpdate.html', context)


@superuser_required
def razorPayGatewayView(request):
    rpg_settings = RazorPayGateway.objects.first()

    if request.method == 'POST':
        # If settings exist, update the existing one
        if rpg_settings:
            rpg_form = RazorPayGatewayForm(request.POST, instance=rpg_settings)
        # If no settings are available, create a new one
        else:
            rpg_form = RazorPayGatewayForm(request.POST)

        if rpg_form.is_valid():
            if not rpg_settings or rpg_form.has_changed():
                rpg_form.save()
                if rpg_settings:
                    messages.success(request, 'Your payment gateway settings have been updated.')
                else:
                    messages.success(request, 'Your payment gateway settings have been saved.')
                return redirect('razorPayGatewayView')
            else:
                messages.info(request, 'Nothing has changed.')
        else:
            messages.error(request, 'There was an error in your form.')
    else:
        if rpg_settings:
            rpg_form = RazorPayGatewayForm(instance=rpg_settings)
        else:
            rpg_form = RazorPayGatewayForm()

    context = {
        'rpg_settings': rpg_settings,
        'rpg_form': rpg_form,
    }
    return render(request, 'be/apps/settings/razorPayGatewayUpdate.html', context)

@superuser_required
def messagingAPIView(request):
    twilio_settings = Twilio.objects.first()

    if twilio_settings is None:
        if request.method == 'POST':
            msg_form = TwilioForm(request.POST)
            if msg_form.is_valid():
                msg_form.save()
                messages.success(request, 'Your settings have been saved.')
                return redirect('messagingAPI')
            else:
                messages.error(request, 'There was an error in your form.')
        else:
            msg_form = TwilioForm()
    else:
        if request.method == 'POST':
            msg_form = TwilioForm(request.POST, instance=twilio_settings)
            if msg_form.is_valid():
                if msg_form.has_changed():
                    msg_form.save()
                    messages.success(request, 'Your settings have been updated.')
                    return redirect('messagingAPI')
                else:
                    messages.info(request, 'Nothing has changed.')
            else:
                messages.error(request, 'There was an error in your form.')
        else:
            msg_form = TwilioForm(instance=twilio_settings)

    context = {
        'twilio_settings': twilio_settings,
        'msg_form': msg_form,
    }
    return render(request, 'be/apps/settings/messageAPIUpdate.html', context)


def changeLogView(request):
    all_changelog = Changelog.objects.all().order_by('-created')
    context = {
        'all_changelog': all_changelog,
    }
    return render(request, 'be/apps/settings/changelog/view.html', context)


@superuser_required
def countryView(request):
    countryQuerySet = Country.objects.select_related().order_by('-name')
    countrySearch = ""  # Default to empty string

    # Handle search functionality
    if request.method == 'POST':
        countrySearch = request.POST.get('countrySearch', "")
        if countrySearch:
            countryQuerySet = countryQuerySet.filter(
                Q(name__icontains=countrySearch) |
                Q(iso3__icontains=countrySearch) |
                Q(iso2__icontains=countrySearch) |
                Q(phone_code__icontains=countrySearch) |
                Q(currency__icontains=countrySearch)
            )

    # Handle pagination
    items_per_page = int(request.GET.get('items', 10))  # Defaulted to 10
    paginator = Paginator(countryQuerySet, items_per_page)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_countries = paginator.get_page(page_number)

    context = {
        'allCountry': paged_countries,
        'countrySearch': countrySearch,
    }
    return render(request, 'be/apps/settings/country/read.html', context)


@superuser_required
def countryAddView(request):
    if request.method == 'POST':
        country_form = CountryForm(request.POST)
        if country_form.is_valid():
            name = country_form.cleaned_data['name']
            iso3 = country_form.cleaned_data['iso3']
            iso2 = country_form.cleaned_data['iso2']
            numeric_code = country_form.cleaned_data['numeric_code']
            phone_code = country_form.cleaned_data['phone_code']
            capital = country_form.cleaned_data['capital']
            currency = country_form.cleaned_data['currency']
            tld = country_form.cleaned_data['tld']
            native = country_form.cleaned_data['native']
            region = country_form.cleaned_data['region']
            sub_region = country_form.cleaned_data['sub_region']
            timezones = country_form.cleaned_data['timezones']
            latitude = country_form.cleaned_data['latitude']
            longitude = country_form.cleaned_data['longitude']
            emoji = country_form.cleaned_data['emoji']
            emojiU = country_form.cleaned_data['emojiU']
            status = country_form.cleaned_data['status']
            country = Country.objects.create_user(
                name=name, iso3=iso3, iso2=iso2, numeric_code=numeric_code, phone_code=phone_code, capital=capital,
                currency=currency, tld=tld, native=native, region=region, sub_region=sub_region, timezones=timezones,
                latitude=latitude, longitude=longitude, emoji=emoji, emojiU=emojiU, status=status,
            )
            country.save()
            messages.success(request, 'Country has been created.')
            return redirect('countryList')
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        country_form = CountryForm()

    context = {
        'country_form': country_form,
    }
    return render(request, 'be/apps/settings/country/create.html', context)


@superuser_required
def countryUpdateView(request, pk):
    singleCountry = get_object_or_404(Country, id=pk)
    if request.method == 'POST':
        country_form = CountryForm(request.POST, instance=singleCountry)
        if country_form.is_valid():
            if country_form.has_changed():
                country_form.save()
                messages.success(request, 'Country has been updated.')
                return redirect('countryList')
            else:
                messages.info(request, 'Nothing has changed.')
    else:
        country_form = CountryForm(instance=singleCountry)

    context = {
        'singleCountry': singleCountry,
        'country_form': country_form,
    }
    return render(request, 'be/apps/settings/country/update.html', context)


@superuser_required
def stateListView(request):
    # Look for 'stateSearch' in both POST and GET requests to support pagination
    stateSearch = request.POST.get('stateSearch', '') or request.GET.get('stateSearch', '').strip()

    if stateSearch:
        matching_countries = Country.objects.filter(name__icontains=stateSearch)
        if matching_countries.exists():
            allStates = (State.objects.filter
            (country__in=matching_countries).select_related('country').order_by('-name'))
        else:
            allStates = (State.objects.filter
            (name__icontains=stateSearch).select_related('country').order_by('-name'))
    else:
        allStates = State.objects.select_related('country').order_by('-name')

    paginator = Paginator(allStates, per_page=20)
    page = request.GET.get('page')
    paged_allStates = paginator.get_page(page)

    context = {
        'allStates': paged_allStates,
        'stateSearch': stateSearch,
    }
    return render(request, 'be/apps/settings/state/read.html', context)


@superuser_required
def stateAddView(request):
    if request.method == 'POST':
        state_form = StateForm(request.POST)
        if state_form.is_valid():
            name = state_form.cleaned_data['name']
            country = state_form.cleaned_data['country']
            state_code = state_form.cleaned_data['state_code']
            type = state_form.cleaned_data['type']
            latitude = state_form.cleaned_data['latitude']
            longitude = state_form.cleaned_data['longitude']
            status = state_form.cleaned_data['status']
            state = State.objects.create_user(
                name=name,
                country=country,
                state_code=state_code,
                type=type,
                latitude=latitude,
                longitude=longitude,
                status=status,
            )
            state.save()
            messages.success(request, 'State has been created.')
            return redirect('stateList')
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        state_form = StateForm()

    context = {
        'state_form': state_form,
    }
    return render(request, 'be/apps/settings/state/create.html', context)


@superuser_required
def stateUpdateView(request, pk):
    singleState = get_object_or_404(State, id=pk)
    if request.method == 'POST':
        state_form = StateForm(request.POST, instance=singleState)
        if state_form.is_valid():
            if state_form.has_changed():
                state_form.save()
                messages.success(request, 'State has been updated.')
                return redirect('stateList')
            else:
                messages.info(request, 'Nothing has changed.')
    else:
        state_form = StateForm(instance=singleState)

    context = {
        'singleState': singleState,
        'state_form': state_form,
    }
    return render(request, 'be/apps/settings/state/update.html', context)


@superuser_required
def cityListView(request):
    citySearch = request.GET.get('citySearch', '').strip()  # Use GET to fetch the search term

    # Adjust the query to filter by city name, state name, or country name
    if citySearch:
        allCities = City.objects.filter(
            Q(name__icontains=citySearch) |
            Q(state__name__icontains=citySearch) |
            Q(country__name__icontains=citySearch)
        ).select_related('country', 'state').order_by('-name')
    else:
        allCities = City.objects.select_related('country', 'state').order_by('-name')

    paginator = Paginator(allCities, per_page=20)  # Show 20 cities per page
    page_number = request.GET.get('page')
    paged_allCities = paginator.get_page(page_number)

    context = {
        'allCities': paged_allCities,
        'citySearch': citySearch,  # Include the search term in the context
    }

    return render(request, 'be/apps/settings/city/read.html', context)


@superuser_required
def cityAddView(request):
    if request.method == 'POST':
        city_form = StateForm(request.POST)
        if city_form.is_valid():
            name = city_form.cleaned_data['name']
            country = city_form.cleaned_data['country']
            state = city_form.cleaned_data['state']
            latitude = city_form.cleaned_data['latitude']
            longitude = city_form.cleaned_data['longitude']
            status = city_form.cleaned_data['status']
            city = City.objects.create_user(
                name=name,
                country=country,
                state=state,
                latitude=latitude,
                longitude=longitude,
                status=status,
            )
            city.save()
            messages.success(request, 'City has been created.')
            return redirect('cityList')
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        city_form = CityForm()

    context = {
        'city_form': city_form,
    }
    return render(request, 'be/apps/settings/city/create.html', context)


@superuser_required
def cityUpdateView(request, pk):
    singleCity = get_object_or_404(City, id=pk)
    if request.method == 'POST':
        city_form = CityForm(request.POST, instance=singleCity)
        if city_form.is_valid():
            city_form.save()
            messages.success(request, 'State has been updated.', extra_tags='alert-success')
            return redirect('cityList')
    else:
        city_form = CityForm(instance=singleCity)

    context = {
        'singleCity': singleCity,
        'city_form': city_form,
    }
    return render(request, 'be/apps/settings/city/update.html', context)


@superuser_required
def membershipListView(request):
    membershipSearch = request.GET.get('membershipSearch', '').strip()  # Use GET to fetch the search term

    # Adjust the query to filter by city name, state name, or country name
    if membershipSearch:
        allMembership = Membership.objects.filter(
            Q(title__icontains=membershipSearch) |
            Q(type__icontains=membershipSearch) |
            Q(duration__icontains=membershipSearch)
        ).order_by('-created_date')
    else:
        allMembership = Membership.objects.all().order_by('-created_date')

    paginator = Paginator(allMembership, per_page=20)  # Show 20 cities per page
    page_number = request.GET.get('page')
    paged_allMembership = paginator.get_page(page_number)

    context = {
        'allMembership': paged_allMembership,
        'membershipSearch': membershipSearch,  # Include the search term in the context
    }

    return render(request, 'be/apps/settings/membership/read.html', context)


@superuser_required
def membershipAddView(request):
    if request.method == 'POST':
        mForm = MembershipForm(request.POST)
        if mForm.is_valid():
            # Here you can check form field values and make changes if necessary
            membership = mForm.save(commit=False)
            # Save the Membership instance
            membership.save()
            messages.success(request, 'Membership added successfully.')
            return redirect('membershipList')  # Adjust redirect to the correct URL name
    else:
        mForm = MembershipForm()

    context = {
        'mForm': mForm,
    }

    return render(request, 'be/apps/settings/membership/create.html', context)


@superuser_required
def membershipUpdateView(request, pk):
    # Retrieve the Membership object by its primary key (pk)
    membership = get_object_or_404(Membership, id=pk)
    if request.method == 'POST':
        # Populate the form with the submitted data and the instance to be updated
        mForm = MembershipForm(request.POST, instance=membership)
        if mForm.is_valid():
            mForm.save()
            messages.success(request, 'Membership updated successfully.')
            return redirect('membershipList')  # Adjust with the correct name of your membership list view
    else:
        # Populate the form with data from the existing Membership instance
        mForm = MembershipForm(instance=membership)

    context ={
        'mForm': mForm,
        'membership': membership
    }

    return render(request, 'be/apps/settings/membership/update.html', context)


@superuser_required
def membershipDeleteView(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if request.method == 'POST':
        membership.delete()
        messages.success(request, 'Membership deleted successfully.')
        return redirect('membershipList')  # Redirect to the membership list view
    context = {
        'membership': membership
    }
    return render(request, 'be/apps/settings/membership/delete.html', context)


@require_POST
@login_required
@csrf_exempt
def add_service(request):
    name = request.POST.get('name')
    if name:
        service, created = Services.objects.get_or_create(title=name)
        return JsonResponse({'success': True, 'service_id': service.id})
    return JsonResponse({'success': False})