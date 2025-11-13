from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

def order_create(request):
    """
    Handles order creation during the checkout process.

    Steps:
    1. Retrieves the shopping cart.
    2. On POST, validates the order form and saves the order.
    3. Associates coupon and discount if applied.
    4. Creates OrderItem instances for each cart item.
    5. Clears the cart and triggers asynchronous email task.
    6. Stores order ID in session and redirects to payment process.

    Args:
        request (HttpRequest): Incoming request object.

    Returns:
        HttpResponse: Renders order creation form or redirects to payment.
    """
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Apply coupon if available in cart
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.save()

            # Create OrderItem for each cart item
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()

            # Send asynchronous confirmation email
            order_created.delay(order.id)

            # Save order ID in session for payment process
            request.session['order-id'] = order.id

            # Redirect to payment processing page
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    context = {
        'cart': cart,
        'form': form
    }

    return render(request, 'orders/order/create.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Renders detailed view of a specific order for admin users.

    Args:
        request (HttpRequest): Incoming request object.
        order_id (int): ID of the order to display.

    Returns:
        HttpResponse: Rendered admin order detail page.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generates a PDF invoice for a specific order for admin users.

    Steps:
    1. Retrieve the order by ID.
    2. Render the order to HTML template.
    3. Convert HTML to PDF using WeasyPrint.
    4. Return PDF as HttpResponse.

    Args:
        request (HttpRequest): Incoming request object.
        order_id (int): ID of the order.

    Returns:
        HttpResponse: PDF file response with order invoice.
    """
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response, 
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    )
    return response
