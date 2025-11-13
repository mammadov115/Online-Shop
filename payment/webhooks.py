import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed

@csrf_exempt
def stripe_webhook(request):
    """
    Handles incoming Stripe webhook events.
    
    This endpoint:
    1. Verifies the Stripe webhook signature to ensure authenticity.
    2. Processes 'checkout.session.completed' events.
    3. Marks the corresponding Order as paid and triggers invoice email via Celery.
    
    Args:
        request (HttpRequest): Incoming webhook request from Stripe.
    
    Returns:
        HttpResponse: HTTP 200 for success, 400 for bad request, 404 if order not found.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    # Verify the webhook signature
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle checkout session completion
    if event.type == 'checkout.session.completed':
        session = event.data.object

        # Only process successful payments
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                # Retrieve the order linked via client_reference_id
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            # Mark the order as paid
            order.paid = True
            order.save()

            # Trigger asynchronous invoice email task
            payment_completed.delay(order.id)

    # Return 200 to acknowledge receipt of the webhook
    return HttpResponse(status=200)
