from django.urls import path
from . import views

# Namespace for this Django app's URLs
app_name = 'shop'


# URL patterns for the shop application.
# Handles:
# - Product list view (all products or filtered by category)
# - Product detail view (specific product by ID and slug)


urlpatterns = [
	# Displays all available products
	path('',views.product_list,name='product_list'),

	# Displays products filtered by category slug
	path('<slug:category_slug>/',views.product_list,name='product_list_by_category'),

	# Displays a specific product detail page
	path('<int:id>/<slug:slug>/',views.product_detail,name='product_detail')
]
