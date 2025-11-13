from django.urls import path
from . import views
from . import webhooks

# Namespace for the payment app
app_name = 'payment'

# URL configuration for payment processing and Stripe webhook handling.
# Handles:
# - payment initiation
# - success and cancellation callbacks
# - Stripe webhook events for asynchronous updates

urlpatterns = [
    # Route to initiate the payment process
    path('process/', views.payment_process, name='process'),

    # Route displayed after successful payment completion
    path('completed/', views.payment_completed, name='completed'),

    # Route displayed when payment is canceled or fails
    path('canceled/', views.payment_canceled, name='canceled'),

    # Stripe webhook endpoint to receive asynchronous payment event notifications
    path("webhook/", webhooks.stripe_webhook, name="stripe-webhook"),
]
