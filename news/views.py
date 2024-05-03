import logging
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Q, OuterRef, Exists
from django.contrib.auth.decorators import login_required
from .models import News
from .forms import NewsForm
from core.decorators import superuser_required

# Get an instance of a logger
logger = logging.getLogger(__name__)

User = get_user_model()


def news(request):
    all_news = News.objects.order_by('-created_date').filter(status='Active')
    paginator = Paginator(all_news, 12)
    page = request.GET.get('page')
    paged_news = paginator.get_page(page)
    data = {
        'all_news': paged_news,
    }
    return render(request, 'front/news/news.html', data)


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)

    # Initialize the session key for tracking viewed news if not already done
    if 'viewed_news' not in request.session:
        request.session['viewed_news'] = []

    # Check if the news has been viewed in this session
    if news.id not in request.session['viewed_news']:
        # Increment views because this is a new view
        news.views += 1
        news.save()

        # Mark this news as viewed in this session
        viewed_news = request.session['viewed_news']
        viewed_news.append(news.id)
        request.session['viewed_news'] = viewed_news  # Update the session

    data = {
        'news': news,
    }
    return render(request, 'front/news/news_detail.html', data)


@superuser_required
def filter_news(news_queryset, filter_value):
    # Filter news based on the filter_value
    if filter_value == 'Published':
        news_queryset = news_queryset.filter(status='Published')
    elif filter_value == 'Draft':
        news_queryset = news_queryset.filter(status='Draft')
    elif filter_value == 'Review':
        news_queryset = news_queryset.filter(status='Review')
    elif filter_value == 'Rejected':
        news_queryset = news_queryset.filter(status='Rejected')

    return news_queryset.order_by('-created_date')

@superuser_required
@login_required
def newsListView(request):
    currentUser = request.user

    # Start with all news
    # Show all news to superusers, otherwise show user-specific news
    if currentUser.is_superuser:
        newsQuerySet = News.objects.all()
    else:
        # This is an example, adjust the filter based on your model relationships and requirements
        newsQuerySet = News.objects.filter(author=currentUser)

    filter_value = request.POST.get('filterSelect')

    # Apply filtering if filter value is provided
    if filter_value and filter_value != 'all':
        newsQuerySet = filter_news(newsQuerySet, filter_value)

    # Handle search functionality
    if request.method == 'POST':
        tSearch = request.POST.get('newsSearch')
        if tSearch:
            newsQuerySet = newsQuerySet.filter(
                Q(title__icontains=tSearch) |
                Q(location__icontains=tSearch)
            )

    # Reverse the ordering to show latest news first
    newsQuerySet = newsQuerySet.order_by('-created_date')

    # Handle pagination
    items_per_page = int(request.GET.get('items', 10))  # Defaulted to 10
    paginator = Paginator(newsQuerySet, items_per_page)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_news = paginator.get_page(page_number)

    context = {
        'allNews': paged_news,
        'items_per_page': items_per_page,
        'filter_value': filter_value,
    }
    return render(request, 'be/apps/news/read.html', context)


@superuser_required
@login_required
def newsAddView(request):
    current_user = request.user
    if request.method == 'POST':
        nForm = NewsForm(request.POST, request.FILES, user=current_user)
        if nForm.is_valid():
            news = nForm.save(commit=False)
            news.author = request.user
            news.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # For AJAX requests, respond with JSON including redirect URL
                return JsonResponse({
                    'success': True,
                    'message': 'News added successfully.',
                    'redirect_url': reverse('newsList')  # Provide the URL to redirect to
                })
            else:
                messages.success(request, 'News added successfully.')
                return redirect('newsList')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': nForm.errors}, status=400)
            messages.error(request, 'Please correct the errors below.')
    else:
        nForm = NewsForm()

    context = {
        'nForm': nForm,
    }

    return render(request, 'be/apps/news/create.html', context)


@superuser_required
@login_required
def newsEditView(request, pk):
    news = get_object_or_404(News, id=pk)
    if request.method == 'POST':
        nForm = NewsForm(request.POST, request.FILES, instance=news)
        if nForm.is_valid():
            news = nForm.save(commit=False)
            news.save()
            messages.success(request, 'News updated successfully.')
            return redirect('newsList')  # Adjust the redirect as necessary
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        nForm = NewsForm(instance=news)

    context = {
        'nForm': nForm,
        'news': news
    }

    return render(request, 'be/apps/news/update.html', context)


@superuser_required
@login_required(login_url='login')
def newsDeletetView(request, pk):
    currentUser = request.user
    news = get_object_or_404(News, id=pk)
    if currentUser.is_superuser or currentUser.is_admin or currentUser == news.author:
        if request.method == "POST":
            news.delete()
            messages.success(request, 'You have successfully deleted the news!')
            return redirect('newsList')
    else:
        messages.error(request, 'You do not have permission to delete this news.')

    context = {
        'news': news,
    }
    return render(request, 'be/apps/news/delete.html', context)