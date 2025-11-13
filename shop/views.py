from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender

# Views for the shop application.
# Handles product listing, category filtering, and detailed product pages with recommendations.


def product_list(request, category_slug=None):
    """
    Display a list of available products.
    
    If a category slug is provided, filter the products by that category.
    Supports multilingual category lookup using django-parler's translation system.
    
    Args:
        request (HttpRequest): The incoming HTTP request object.
        category_slug (str, optional): The slug of the category to filter products by.
    
    Returns:
        HttpResponse: Rendered HTML page displaying a list of products.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        # Fetch the current request's active language
        language = request.LANGUAGE_CODE

        # Get category for the current language and slug
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug
        )

        # Filter products belonging to the selected category
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }

    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    """
    Display detailed information about a single product.
    
    Also provides a form to add the product to the cart and 
    shows recommended products using the Redis-based Recommender system.
    
    Args:
        request (HttpRequest): The incoming HTTP request object.
        id (int): The ID of the product.
        slug (str): The slug of the product for SEO-friendly URLs.
    
    Returns:
        HttpResponse: Rendered HTML page displaying product details, 
                      add-to-cart form, and related product suggestions.
    """
    # Retrieve the product or return 404 if not found
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # Form for adding product to the shopping cart
    cart_product_form = CartAddProductForm()

    # Instantiate recommender and fetch top 4 similar products
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
    }

    return render(request, 'shop/product/detail.html', context)
