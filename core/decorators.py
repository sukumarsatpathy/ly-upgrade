from functools import wraps
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from subscription.models import Subscription


def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to log in
        if not request.user.is_superuser:
            return redirect('dashboard')  # Or HttpResponseForbidden() if you prefer a 403 response
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_auth_or_superuser_edit_view(model, redirect_url='dashboard'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Ensure the view is receiving 'pk' keyword argument
            pk = kwargs.get('pk')
            if pk is None:
                return HttpResponse("Error: Missing 'pk' argument.", status=400)
            # Retrieve the object using 'pk'
            obj = get_object_or_404(model, pk=pk)
            # Permission check: User must be superuser or the author
            if not (request.user.is_superuser or obj.author_id == request.user.id):
                return redirect(redirect_url)
            # Proceed with the original view
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# For Checking User Membership
def user_has_active_membership(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Allow superusers to bypass the subscription check
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to access this page.")
            return redirect('login')

        # Check for any active subscription that has not expired for general users.
        has_active_subscription = Subscription.objects.filter(
            user=request.user,
            status='Active',
            endDate__gte=timezone.now()  # Ensure your model's field is named `expiry_date`, not `endDate`
        ).exists()

        if not has_active_subscription:
            messages.error(request, "You need an active subscription to access this page.")
            return redirect('membership-renewal')

        return view_func(request, *args, **kwargs)
    return _wrapped_view