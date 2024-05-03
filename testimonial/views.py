import logging
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Q, OuterRef, Exists
from django.contrib.auth.decorators import login_required
from .models import Testimonial
from .forms import TestimonialForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

User = get_user_model()


def testimonial(request):
    all_testimonials = Testimonial.objects.order_by('-created_date').filter(status='Published')
    paginator = Paginator(all_testimonials, 12)
    page = request.GET.get('page')
    paged_testimonial = paginator.get_page(page)
    data = {
        'all_testimonials': paged_testimonial,
    }
    return render(request, 'front/testimonial/testimonial.html', data)


def testimonial_detail(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)

    # Initialize the session key for tracking viewed testimonials if not already done
    if 'viewed_testimonials' not in request.session:
        request.session['viewed_testimonials'] = []

    # Check if the testimonial has been viewed in this session
    if testimonial.id not in request.session['viewed_testimonials']:
        # Increment views because this is a new view
        testimonial.views += 1
        testimonial.save()

        # Mark this testimonial as viewed in this session
        viewed_testimonials = request.session['viewed_testimonials']
        viewed_testimonials.append(testimonial.id)
        request.session['viewed_testimonials'] = viewed_testimonials  # Update the session

    context = {
        'single_testimonial': testimonial,
    }
    return render(request, 'front/testimonial/testimonial_detail.html', context)


def filter_testimonials(testimonials_queryset, filter_value):
    # Filter testimonials based on the filter_value
    if filter_value == 'Published':
        testimonials_queryset = testimonials_queryset.filter(status='Published')
    elif filter_value == 'Draft':
        testimonials_queryset = testimonials_queryset.filter(status='Draft')
    elif filter_value == 'Review':
        testimonials_queryset = testimonials_queryset.filter(status='Review')
    elif filter_value == 'Rejected':
        testimonials_queryset = testimonials_queryset.filter(status='Rejected')

    return testimonials_queryset.order_by('-created_date')


def testimonialListView(request):
    currentUser = request.user

    # Start with all testimonials
    # Show all testimonials to superusers, otherwise show user-specific testimonials
    if currentUser.is_superuser:
        testimonialsQuerySet = Testimonial.objects.all()
    else:
        # This is an example, adjust the filter based on your model relationships and requirements
        testimonialsQuerySet = Testimonial.objects.filter(author=currentUser)

    filter_value = request.POST.get('filterSelect')

    # Apply filtering if filter value is provided
    if filter_value and filter_value != 'all':
        testimonialsQuerySet = filter_testimonials(testimonialsQuerySet, filter_value)

    # Handle search functionality
    if request.method == 'POST':
        tSearch = request.POST.get('testimonialSearch')
        if tSearch:
            testimonialsQuerySet = testimonialsQuerySet.filter(
                Q(title__icontains=tSearch) |
                Q(publisher__icontains=tSearch) |
                Q(location__icontains=tSearch)
            )

    # Reverse the ordering to show latest testimonials first
    testimonialsQuerySet = testimonialsQuerySet.order_by('-created_date')

    # Handle pagination
    items_per_page = int(request.GET.get('items', 25))  # Defaulted to 10
    paginator = Paginator(testimonialsQuerySet, items_per_page)  # Adjust items_per_page as needed
    page_number = request.GET.get('page')
    paged_testimonials = paginator.get_page(page_number)

    context = {
        'allTestimonials': paged_testimonials,
        'items_per_page': items_per_page,
        'filter_value': filter_value,
    }
    return render(request, 'be/apps/testimonial/read.html', context)


@login_required
def testimonialAddView(request):
    current_user = request.user
    if request.method == 'POST':
        tForm = TestimonialForm(request.POST, request.FILES, user=current_user)
        if tForm.is_valid():
            testimonial = tForm.save(commit=False)
            if not current_user.is_superuser:
                testimonial.author = request.user
                testimonial.status = "Review"
            testimonial.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # For AJAX requests, respond with JSON including redirect URL
                return JsonResponse({
                    'success': True,
                    'message': 'Testimonial added successfully.',
                    'redirect_url': reverse('testimonialList')  # Provide the URL to redirect to
                })
            else:
                messages.success(request, 'Testimonial added successfully.')
                return redirect('testimonialList')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': tForm.errors}, status=400)
            messages.error(request, 'Please correct the errors below.')
    else:
        tForm = TestimonialForm(user=request.user)

    context = {
        'tForm': tForm,
    }

    return render(request, 'be/apps/testimonial/create.html', context)


@login_required
def testimonialEditView(request, pk):
    testimonial = get_object_or_404(Testimonial, id=pk)

    # Check if the current user is allowed to edit this testimonial
    if not request.user.is_superuser and testimonial.author != request.user:
        messages.error(request, "You do not have permission to edit this testimonial.")
        return redirect('testimonialList')

    if request.method == 'POST':
        tForm = TestimonialForm(request.POST, request.FILES, instance=testimonial, user=request.user)
        if tForm.is_valid():
            if not tForm.has_changed():
                # If the form has not changed, redirect to the list page with a message
                messages.info(request, "Nothing has changed.")
                return redirect('testimonialList')

            edited_testimonial = tForm.save(commit=False)
            # Ensure the testimonial maintains its association with the original author
            edited_testimonial.author = testimonial.author

            # Set status based on the user role
            if not request.user.is_superuser:
                edited_testimonial.status = 'Review'

            edited_testimonial.save()
            messages.success(request, 'Testimonial updated successfully.')
            return redirect('testimonialList')  # Adjust the redirect as necessary
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        tForm = TestimonialForm(instance=testimonial, user=request.user)

    context = {
        'tForm': tForm,
        'testimonial': testimonial
    }

    return render(request, 'be/apps/testimonial/update.html', context)


@login_required(login_url='login')
def testimonialDeleteView(request, pk):
    currentUser = request.user
    testimonial = get_object_or_404(Testimonial, id=pk)
    if currentUser.is_superuser or currentUser.is_admin or currentUser == testimonial.author:
        if request.method == "POST":
            testimonial.delete()
            messages.success(request, 'You have successfully deleted the testimonial!')
            return redirect('testimonialList')
    else:
        messages.error(request, 'You do not have permission to delete this testimonial.')

    context = {
        'testimonial': testimonial,
    }
    return render(request, 'be/apps/testimonial/delete.html', context)