from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """
    Celery task to send an order confirmation email to the customer.

    This task:
    1. Retrieves the order by its ID.
    2. Composes an email with order details.
    3. Sends the email asynchronously via Celery.

    Args:
        order_id (int): The ID of the created order.

    Returns:
        int: Number of successfully delivered messages (as returned by send_mail).
    """
    # Retrieve the order from the database
    order = Order.objects.get(id=order_id)

    # Email subject and body
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\nYou have successfully placed an order. Your order ID is {order.id}'

    # Send email asynchronously
    mail_sent = send_mail(
        subject,
        message,
        'admin@myshop',  # From email
        [order.email]     # Recipient list
    )

    return mail_sent
