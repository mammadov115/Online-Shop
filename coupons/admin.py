from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Coupon model.

    Features:
    - Displays key fields in the list view.
    - Filters for active status and validity dates.
    - Provides search by coupon code for quick lookup.
    """
    # Fields to display in the admin list view
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']

    # Filters available in the right sidebar
    list_filter = ['active', 'valid_from', 'valid_to']

    # Search box to find coupons by code
    search_fields = ['code']
