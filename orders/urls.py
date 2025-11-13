from django.urls import path
from . import views

# Namespace for the orders app
app_name = 'orders'

# URL configuration for handling order creation and admin views
urlpatterns = [
    # Public route to create a new order during checkout
    path("create/", views.order_create, name="order_create"),

    # Admin route to view detailed information about a specific order
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),

    # Admin route to generate/download PDF invoice for a specific order
    path("admin/order/<int:order_id>/pdf/", views.admin_order_pdf, name="admin_order_pdf"),
]
