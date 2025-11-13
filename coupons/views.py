from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def coupon_apply(request):
    """
    Applies a valid coupon to the current user's session.

    Steps:
    1. Only allows POST requests (form submission).
    2. Validates the coupon form submitted by the user.
    3. Checks if the coupon exists, is active, and within valid date range.
    4. Stores the coupon ID in the user's session for later use during checkout.
    5. If the coupon is invalid, removes any previously stored coupon from session.
    6. Redirects user back to the cart detail page.

    Args:
        request (HttpRequest): The incoming HTTP request with coupon data.

    Returns:
        HttpResponseRedirect: Redirects to the cart detail page.
    """
    now = timezone.now()  # Current datetime for validity check

    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']

        try:
            # Check for an active coupon within its valid period
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            # Save coupon ID in session to apply during checkout
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            # Remove coupon from session if invalid
            request.session['coupon_id'] = None

    # Redirect back to the cart page
    return redirect('cart:cart_detail')
