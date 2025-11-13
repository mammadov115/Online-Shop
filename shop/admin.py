from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin

# Register your models here.
# Django admin configuration for Category and Product models.
# Category uses django-parler for multilingual field management.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """
    Admin configuration for the Category model.
    
    Uses django-parler's TranslatableAdmin to handle multilingual fields.
    Automatically populates the `slug` field based on the `name`.
    """
	list_display = ['name','slug']
	# for django-parler
	# prepopulated_fields = {'slug':('name',)}
	def get_prepopulated_fields(self, request, obj=None):
        """
        Defines fields that should be automatically populated.
        Here, the `slug` is generated from the `name` field.
        """
		return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    
    Provides quick access to key product details, filtering, and 
    inline editing of selected fields in the admin panel.
    """

    # Fields displayed in the list view
	list_display = ['name','slug','price','available','created','updated']
    # Filters available in the sidebar
	list_filter = ['available','created','updated']
 	# Fields editable directly from the list view
	list_editable = ['price','available']
	# Automatically populate slug based on name
	prepopulated_fields = {'slug':('name',)}



