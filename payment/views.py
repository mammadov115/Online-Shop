from django.shortcuts import render, redirect, reverse, get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order

# Configure Stripe API key and version
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    """
    Handles the payment process for an order using Stripe Checkout.
    
    Steps:
    1. Retrieve the order ID from the session.
    2. If POST request, create a Stripe Checkout session with all order items.
       - Convert item prices to the smallest currency unit (e.g., qəpik for AZN).
       - Include coupon discount if available.
    3. Redirect the user to Stripe Checkout or render the payment page for GET requests.
    
    Args:
        request (HttpRequest): The incoming HTTP request object.
    
    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to Stripe Checkout or renders the payment page.
    """
    order_id = request.session.get('order-id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # URLs for redirection after payment success or cancellation
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Prepare Stripe Checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # Add each order item to Stripe Checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),  # convert to qəpik
                    'currency': 'azn',
                    'product_data': {
                        'name': item.product.name
                    },
                },
                'quantity': item.quantity,
            })

        # Apply coupon if exists
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration='once'
            )
            session_data['discounts'] = [{'coupon': stripe_coupon.id}]
            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)
        else:
            # Render local payment page if no coupon
            return render(request, 'payment/process.html', locals())
    else:
        # Render payment page for GET requests
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    """
    Renders the page shown after a successful payment.
    
    Args:
        request (HttpRequest): The incoming HTTP request object.
    
    Returns:
        HttpResponse: Rendered HTML page confirming successful payment.
    """
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    """
    Renders the page shown when payment is canceled or fails.
    
    Args:
        request (HttpRequest): The incoming HTTP request object.
    
    Returns:
        HttpResponse: Rendered HTML page indicating canceled payment.
    """
    return render(request, 'payment/canceled.html')
