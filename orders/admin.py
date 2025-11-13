from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

# ------------------------------
# Helper functions for admin
# ------------------------------

def export_to_csv(modeladmin, request, queryset):
    """
    Admin action to export selected orders to a CSV file.

    Args:
        modeladmin: The admin model instance.
        request: The HTTP request object.
        queryset: The selected objects queryset.

    Returns:
        HttpResponse: CSV file containing order data.
    """
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    # Get all fields except ManyToMany and reverse relations
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    
    # Write header row
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    
    return response

export_to_csv.short_description = "Export to CSV"


def order_detail(obj):
    """
    Returns a clickable link to view the order details in admin.

    Args:
        obj: Order instance.

    Returns:
        Safe HTML string containing link.
    """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f"<a href='{url}'>View</a>")


def order_pdf(obj):
    """
    Returns a clickable link to download the invoice PDF for the order.

    Args:
        obj: Order instance.

    Returns:
        Safe HTML string containing link.
    """
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f"<a href='{url}'>PDF</a>")

order_pdf.short_description = 'Invoice'


# ------------------------------
# Inline admin for OrderItem
# ------------------------------
class OrderItemInline(admin.TabularInline):
    """
    Inline display of OrderItem within the Order admin page.
    Allows editing related products directly in the Order admin.
    """
    model = OrderItem
    raw_id_fields = ['product']  # Display product as ID input to save space


# ------------------------------
# Main admin for Order
# ------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.

    Features:
    - List display of important fields and custom links for detail/PDF.
    - Filtering by paid status, creation and update dates.
    - Inline display of related OrderItems.
    - CSV export action.
    """
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city',
        'paid', 'created', 'updated', order_detail, order_pdf
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
