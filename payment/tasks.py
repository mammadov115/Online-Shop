from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Celery task to send an invoice email once payment is completed.
    
    This task:
    1. Retrieves the order by its ID.
    2. Generates a PDF invoice using WeasyPrint.
    3. Sends the invoice as an email attachment to the customer.

    Args:
        order_id (int): The ID of the completed order.
    """
    # Retrieve the order from the database
    order = Order.objects.get(id=order_id)

    # Email details
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please find attached the invoice for your recent purchase.'
    email = EmailMessage(
        subject,
        message,
        'admin@myshop.com',
        [order.email]  # corrected from order_id.email
    )

    # Render the HTML invoice template
    html = render_to_string('orders/order/pdf.html', {'order': order})

    # Generate PDF from rendered HTML
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach the generated PDF to the email
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # Send the email with the attached invoice
    email.send()
