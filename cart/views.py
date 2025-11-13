from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity.

    Expects POST data from CartAddProductForm.
    Redirects to the cart detail page after adding.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): ID of the product to add.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        # Add product to cart with optional quantity override
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): ID of the product to remove.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    Display cart contents, allow quantity updates, and show recommended products.

    Includes:
    - Update quantity forms for each item
    - Coupon application form
    - Recommended products based on current cart items
    """
    cart = Cart(request)

    # Add update quantity form to each cart item
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )

    coupon_apply_form = CouponApplyForm()

    # Generate recommended products based on items currently in the cart
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        'recommended_products': recommended_products
    }

    return render(request, 'cart/detail.html', context)
