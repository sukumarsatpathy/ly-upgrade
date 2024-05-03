import logging
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.decorators import superuser_required, user_has_active_membership
from .models import ProDiary, ProResearch, ProVideos, ProDownloads, ProPhotosCat, ProPhotos, ProQuotes
from .forms import ProDiaryForm, ProResearchForm, ProVideosForm, ProDownloadsForm, ProPhotosForm, ProQuotesForm


# Get an instance of a logger
logger = logging.getLogger(__name__)


def prozoneLanding(request):
    return render(request, 'front/pages/prozone-landing-page.html')


@user_has_active_membership
def videoList(request):
    all_pro_videos = ProVideos.objects.all().order_by('-created_date')
    paginator = Paginator(all_pro_videos, 20)
    page = request.GET.get('page')
    paged_all_pro_videos = paginator.get_page(page)
    data = {
        'all_pro_videos': paged_all_pro_videos,
    }
    return render(request, 'fe/prozone/video-layout.html', data)


# Diary Section
@user_has_active_membership
def prodiaryList(request):
    all_diary_articles = ProDiary.objects.all().order_by('-created_date')
    paginator = Paginator(all_diary_articles, 40)
    page = request.GET.get('page')
    paged_all_diary_articles = paginator.get_page(page)
    data = {
        'all_diary_articles': paged_all_diary_articles,
    }
    return render(request, 'fe/prozone/diary/list-layout.html', data)


@user_has_active_membership
def prodiarydetail(request, slug):
    diary_detail = get_object_or_404(ProDiary, slug=slug)
    diary_detail.views = diary_detail.views + 1
    diary_detail.save()
    data = {
        'diary_detail': diary_detail,
    }
    return render(request, 'fe/prozone/diary/detailed-layout.html', data)


# Diary Section
@user_has_active_membership
def proresearchList(request):
    all_research_articles = ProResearch.objects.all().order_by('-created_date')
    paginator = Paginator(all_research_articles, 40)
    page = request.GET.get('page')
    paged_all_research_articles = paginator.get_page(page)
    data = {
        'all_research_articles': paged_all_research_articles,
    }
    return render(request, 'fe/prozone/research-articles/list-layout.html', data)


@user_has_active_membership
def proresearchdetail(request, slug):
    research_detail = get_object_or_404(ProResearch, slug=slug)
    research_detail.views = research_detail.views + 1
    research_detail.save()
    data = {
        'research_detail': research_detail,
    }
    return render(request, 'fe/prozone/research-articles/detailed-layout.html', data)


@user_has_active_membership
def downloadList(request):
    all_downloads = ProDownloads.objects.all().order_by('-created_date')
    paginator = Paginator(all_downloads, 20)
    page = request.GET.get('page')
    paged_all_downloads = paginator.get_page(page)
    data = {
        'all_downloads': paged_all_downloads,
    }
    return render(request, 'fe/prozone/download-layout.html', data)


# Download Photos
@user_has_active_membership
def downloadPhotosList(request):
    all_downloads = ProPhotos.objects.all().order_by('-created_date')
    paginator = Paginator(all_downloads, 20)
    page = request.GET.get('page')
    paged_all_downloads = paginator.get_page(page)
    data = {
        'all_downloads': paged_all_downloads,
    }
    return render(request, 'fe/prozone/download-photos/landing-page.html', data)


@user_has_active_membership
def downloadCatPhotosList(request, cat_slug):
    single_cat_downloads = ProPhotos.objects.filter(category__slug=cat_slug).order_by('-created_date')
    paginator = Paginator(single_cat_downloads, 20)
    page = request.GET.get('page')
    paged_all_downloads = paginator.get_page(page)

    data = {
        'single_cat_downloads': paged_all_downloads,
    }
    return render(request, 'fe/prozone/download-photos/cat-landing-page.html', data)


@user_has_active_membership
def downloadQuoteList(request):
    all_downloads = ProQuotes.objects.all().order_by('-created_date')
    paginator = Paginator(all_downloads, 20)
    page = request.GET.get('page')
    paged_all_downloads = paginator.get_page(page)
    data = {
        'all_downloads': paged_all_downloads,
    }
    return render(request, 'fe/prozone/download-quotes.html', data)


# Admin Code Starts Here
@superuser_required
def proDiaryListView(request):
    allPDLists = ProDiary.objects.all().order_by("-created_date")
    pdSearch = request.GET.get('proDiarySearch', '').strip()
    if pdSearch:
        allPDLists = allPDLists.filter(
            Q(title__icontains=pdSearch)  # Ensure 'title' is a valid field name in your ProDiary model
        )
    paginator = Paginator(allPDLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_diary = paginator.get_page(page_number)
    context = {
        'allPDLists': paged_pro_diary,
    }
    return render(request, 'be/apps/prozone/diary/read.html', context)


@superuser_required
def proDiaryAddView(request):
    if request.method == 'POST':
        pdForm = ProDiaryForm(request.POST, request.FILES)
        if pdForm.is_valid():
            proDiary = pdForm.save(commit=False)
            proDiary.save()
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pdForm = ProDiaryForm(user=request.user)

    context = {
        'pdForm': pdForm,
    }

    return render(request, 'be/apps/prozone/diary/create.html', context)


@superuser_required
def proDiaryEditView(request, slug):
    proDiary = get_object_or_404(ProDiary, slug=slug)
    if request.method == 'POST':
        pdForm = ProDiaryForm(request.POST, request.FILES, instance=proDiary)
        if pdForm.is_valid():
            pdForm.save()
            messages.success(request, 'Pro Diary updated successfully!')
            return redirect('proDiaryList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pdForm = ProDiaryForm(instance=proDiary)  # Populate the form with the existing diary data

    context = {
        'proDiary': proDiary,
        'pdForm': pdForm,
    }
    return render(request, 'be/apps/prozone/diary/update.html', context)


@superuser_required
def proDiaryDeleteView(request, slug):
    proDiary = get_object_or_404(ProDiary, slug=slug)
    if request.method == 'POST':
        proDiary.delete()
        messages.success(request, 'Pro Diary deleted successfully!')
        return redirect('proDiaryList')

    context = {
        'proDiary': proDiary,
    }
    return render(request, 'be/apps/prozone/diary/delete.html', context)


@superuser_required
def raListView(request):
    allPRLists = ProResearch.objects.all().order_by("-created_date")
    prSearch = request.GET.get('search', '').strip()
    if prSearch:
        allPRLists = allPRLists.filter(
            Q(title__icontains=prSearch)  # Ensure 'title' is a valid field name in your ProResearch model
        )
    paginator = Paginator(allPRLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_ra = paginator.get_page(page_number)
    context = {
        'allPRLists': paged_pro_ra,
    }
    return render(request, 'be/apps/prozone/research/read.html', context)


@superuser_required
def raAddView(request):
    if request.method == 'POST':
        prForm = ProResearchForm(request.POST, request.FILES)
        if prForm.is_valid():
            proRA = prForm.save(commit=False)
            proRA.save()
            messages.success(request, 'Research Article published successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        prForm = ProResearchForm()

    context = {
        'prForm': prForm,
    }

    return render(request, 'be/apps/prozone/research/create.html', context)


@superuser_required
def raEditView(request, slug):
    proRA = get_object_or_404(ProResearch, slug=slug)
    if request.method == 'POST':
        prForm = ProResearchForm(request.POST, request.FILES, instance=proRA)
        if prForm.is_valid():
            prForm.save()
            messages.success(request, 'Research Article updated successfully!')
            return redirect('raList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        prForm = ProResearchForm(instance=proRA)  # Populate the form with the existing diary data

    context = {
        'proRA': proRA,
        'prForm': prForm,
    }
    return render(request, 'be/apps/prozone/research/update.html', context)


@superuser_required
def raDeleteView(request, slug):
    proRA = get_object_or_404(ProResearch, slug=slug)
    if request.method == 'POST':
        proRA.delete()
        messages.success(request, 'Research Article deleted successfully!')
        return redirect('raList')

    context = {
        'proRA': proRA,
    }
    return render(request, 'be/apps/prozone/research/delete.html', context)


@superuser_required
def videosListView(request):
    allPVLists = ProVideos.objects.all().order_by("-created_date")
    pvSearch = request.GET.get('search', '').strip()
    if pvSearch:
        allPVLists = allPVLists.filter(
            Q(title__icontains=pvSearch)  # Ensure 'title' is a valid field name in your ProResearch model
        )
    paginator = Paginator(allPVLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_videos = paginator.get_page(page_number)
    context = {
        'allPVLists': paged_pro_videos,
    }
    return render(request, 'be/apps/prozone/videos/read.html', context)


@superuser_required
def videosAddView(request):
    if request.method == 'POST':
        pvForm = ProVideosForm(request.POST, request.FILES)
        if pvForm.is_valid():
            proVideo = pvForm.save(commit=False)
            proVideo.save()
            messages.success(request, 'Video published successfully!')
            return redirect('videosList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pvForm = ProVideosForm()

    context = {
        'pvForm': pvForm,
    }

    return render(request, 'be/apps/prozone/videos/create.html', context)


@superuser_required
def videosEditView(request, slug):
    proVideo = get_object_or_404(ProVideos, slug=slug)
    if request.method == 'POST':
        pvForm = ProVideosForm(request.POST, request.FILES, instance=proVideo)
        if pvForm.is_valid():
            pvForm.save()
            messages.success(request, 'Video updated successfully!')
            return redirect('videosList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pvForm = ProVideosForm(instance=proVideo)  # Populate the form with the existing diary data

    context = {
        'proVideo': proVideo,
        'pvForm': pvForm,
    }
    return render(request, 'be/apps/prozone/videos/update.html', context)


@superuser_required
def videosDeleteView(request, slug):
    proVideo = get_object_or_404(ProVideos, slug=slug)
    if request.method == 'POST':
        proVideo.delete()
        messages.success(request, 'Video deleted successfully!')
        return redirect('videosList')

    context = {
        'proVideo': proVideo,
    }
    return render(request, 'be/apps/prozone/videos/delete.html', context)


@superuser_required
def resourcesListView(request):
    allPDLists = ProDownloads.objects.all().order_by("-created_date")
    pdSearch = request.GET.get('search', '').strip()
    if pdSearch:
        allPDLists = allPDLists.filter(
            Q(title__icontains=pdSearch)  # Ensure 'title' is a valid field name in your ProResearch model
        )
    paginator = Paginator(allPDLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_download = paginator.get_page(page_number)
    context = {
        'allPDLists': paged_pro_download,
    }
    return render(request, 'be/apps/prozone/resources/read.html', context)


@superuser_required
def resourcesAddView(request):
    if request.method == 'POST':
        pdForm = ProDownloadsForm(request.POST, request.FILES)
        if pdForm.is_valid():
            proDownload = pdForm.save(commit=False)
            proDownload.save()
            messages.success(request, 'Resource published successfully!')
            return redirect('resourcesList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pdForm = ProDownloadsForm()

    context = {
        'pdForm': pdForm,
    }

    return render(request, 'be/apps/prozone/resources/create.html', context)


@superuser_required
def resourcesEditView(request, slug):
    proDownload = get_object_or_404(ProDownloads, slug=slug)
    if request.method == 'POST':
        pdForm = ProDownloadsForm(request.POST, request.FILES, instance=proDownload)
        if pdForm.is_valid():
            pdForm.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resourcesList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pdForm = ProDownloadsForm(instance=proDownload)  # Populate the form with the existing diary data

    context = {
        'proDownload': proDownload,
        'pdForm': pdForm,
    }
    return render(request, 'be/apps/prozone/resources/update.html', context)


@superuser_required
def resourcesDeleteView(request, slug):
    proDownload = get_object_or_404(ProDownloads, slug=slug)
    if request.method == 'POST':
        proDownload.delete()
        messages.success(request, 'Resource deleted successfully!')
        return redirect('resourcesList')

    context = {
        'proDownload': proDownload,
    }
    return render(request, 'be/apps/prozone/resources/delete.html', context)


@superuser_required
def photosListView(request):
    allPPLists = ProPhotos.objects.all().order_by("-created_date")
    ppSearch = request.GET.get('search', '').strip()
    if ppSearch:
        allPPLists = allPPLists.filter(
            Q(title__icontains=ppSearch)
        )
    paginator = Paginator(allPPLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_photos = paginator.get_page(page_number)
    context = {
        'allPPLists': paged_pro_photos,
    }
    return render(request, 'be/apps/prozone/photos/read.html', context)


@superuser_required
def photosAddView(request):
    if request.method == 'POST':
        ppForm = ProPhotosForm(request.POST, request.FILES)
        if ppForm.is_valid():
            proPhoto = ppForm.save(commit=False)
            proPhoto.save()
            messages.success(request, 'Photo published successfully!')
            return redirect('photosList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        ppForm = ProPhotosForm()

    context = {
        'ppForm': ppForm,
    }

    return render(request, 'be/apps/prozone/photos/create.html', context)


@superuser_required
def photosEditView(request, slug):
    proPhoto = get_object_or_404(ProPhotos, slug=slug)
    if request.method == 'POST':
        ppForm = ProPhotosForm(request.POST, request.FILES, instance=proPhoto)
        if ppForm.is_valid():
            ppForm.save()
            messages.success(request, 'Photo updated successfully!')
            return redirect('photosList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        ppForm = ProPhotosForm(instance=proPhoto)  # Populate the form with the existing diary data

    context = {
        'proPhoto': proPhoto,
        'ppForm': ppForm,
    }
    return render(request, 'be/apps/prozone/photos/update.html', context)


@superuser_required
def photosDeleteView(request, slug):
    proPhoto = get_object_or_404(ProPhotos, slug=slug)
    if request.method == 'POST':
        proPhoto.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('photosList')

    context = {
        'proPhoto': proPhoto,
    }
    return render(request, 'be/apps/prozone/photos/delete.html', context)


@require_POST
@login_required
@csrf_exempt
def addCategory(request):
    name = request.POST.get('name')
    if name:
        category, created = ProPhotosCat.objects.get_or_create(title=name)
        return JsonResponse({'success': True, 'category_id': category.id})
    return JsonResponse({'success': False})


@superuser_required
def quotesListView(request):
    allPQLists = ProQuotes.objects.all().order_by("-created_date")
    pqSearch = request.GET.get('search', '').strip()
    if pqSearch:
        allPQLists = allPQLists.filter(
            Q(title__icontains=pqSearch)
        )
    paginator = Paginator(allPQLists, 20)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_pro_quotes = paginator.get_page(page_number)
    context = {
        'allPQLists': paged_pro_quotes,
    }
    return render(request, 'be/apps/prozone/quotes/read.html', context)


@superuser_required
def quotesAddView(request):
    if request.method == 'POST':
        pqForm = ProQuotesForm(request.POST, request.FILES)
        if pqForm.is_valid():
            proQuote = pqForm.save(commit=False)
            proQuote.save()
            messages.success(request, 'Quote published successfully!')
            return redirect('quotesList')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pqForm = ProQuotesForm()

    context = {
        'pqForm': pqForm,
    }

    return render(request, 'be/apps/prozone/quotes/create.html', context)


@superuser_required
def quotesEditView(request, slug):
    proQuote = get_object_or_404(ProQuotes, slug=slug)
    if request.method == 'POST':
        pqForm = ProQuotesForm(request.POST, request.FILES, instance=proQuote)
        if pqForm.is_valid():
            pqForm.save()
            messages.success(request, 'Quote updated successfully!')
            return redirect('quotesList')  # Redirect to a success page or the diary detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        pqForm = ProQuotesForm(instance=proQuote)  # Populate the form with the existing diary data

    context = {
        'proQuote': proQuote,
        'pqForm': pqForm,
    }
    return render(request, 'be/apps/prozone/quotes/update.html', context)


@superuser_required
def quotesDeleteView(request, slug):
    proQuote = get_object_or_404(ProQuotes, slug=slug)
    if request.method == 'POST':
        proQuote.delete()
        messages.success(request, 'Quote deleted successfully!')
        return redirect('quotesList')

    context = {
        'proQuote': proQuote,
    }
    return render(request, 'be/apps/prozone/quotes/delete.html', context)