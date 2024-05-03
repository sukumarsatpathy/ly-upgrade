from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Custom App Import
from .models import Subscription
from .forms import SubscriptionForm
from core.decorators import superuser_required


@superuser_required
def subscriptionListView(request):
    subscriptionSearch = request.GET.get('subscriptionSearch', '').strip()

    if subscriptionSearch:
        # Filter subscriptions by subscriptionSearch in user's username, membership title, or active status
        allSubscription = Subscription.objects.filter(
            Q(user__email__icontains=subscriptionSearch) |
            Q(membership__title__icontains=subscriptionSearch)
        ).select_related('user', 'membership').order_by('-start_date')
    else:
        allSubscription = Subscription.objects.all().select_related('user', 'membership').order_by('-startDate')

    context = {
        'allSubscription': allSubscription,
        'subscriptionSearch': subscriptionSearch,
    }
    return render(request, 'be/apps/subscription/read.html', context)


@superuser_required
def subscriptionAddView(request):
    if request.method == 'POST':
        sForm = SubscriptionForm(request.POST)
        if sForm.is_valid():
            new_subscription = sForm.save(commit=False)
            new_subscription.save()
            messages.success(request, 'Subscription added successfully.')
            return redirect('subscriptionList')
    else:
        sForm = SubscriptionForm()

    context = {
        'sForm': sForm,
    }

    return render(request, 'be/apps/subscription/create.html', context)


@superuser_required
def subscriptionEditView(request, pk):
    subscription = get_object_or_404(Subscription, id=pk)
    if request.method == 'POST':
        sForm = SubscriptionForm(request.POST, instance=subscription)
        if sForm.is_valid():
            sForm.save()
            messages.success(request, 'Subscription updated successfully.')
            return redirect('subscriptionList')
    else:
        # GET request, display form with existing subscription details
        sForm = SubscriptionForm(instance=subscription)

    context = {
        'sForm': sForm,
        'subscription': subscription
    }
    return render(request, 'be/apps/subscription/update.html', context)


@superuser_required
def subscriptionDeleteView(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    if request.method == 'POST':
        subscription.delete()
        messages.success(request, 'Subscription successfully deleted.')
        return redirect('subscriptionList')  # Adjust as necessary

    context ={
        'subscription': subscription
    }

    return render(request, 'be/apps/subscription/delete.html', context)