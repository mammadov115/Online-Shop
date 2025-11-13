from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Display the current contents of the shopping cart
    path("", views.cart_detail, name="cart_detail"),

    # Add a product to the cart by product ID
    # Expects POST data from CartAddProductForm
    path("add/<int:product_id>", views.cart_add, name="cart_add"),

    # Remove a product from the cart by product ID
    path("remove/<int:product_id>", views.cart_remove, name="cart_remove")
]
