"""
Root URL configuration for myshop project.

This configuration includes:
- Multilingual URL patterns using `i18n_patterns`
- App namespaces for clear URL resolution
- Static & media file serving in development
- Admin panel with translated URL prefix
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# -----------------------------
# Multilingual URL patterns
# -----------------------------
urlpatterns = i18n_patterns(
    # Admin panel with translated prefix
    path(_('admin/'), admin.site.urls),

    # Shopping cart URLs
    path(_("cart/"), include('cart.urls', namespace="cart")),

    # Orders app URLs
    path(_("orders/"), include('orders.urls', namespace='orders')),

    # Payment app URLs
    path(_('payment/'), include('payment.urls', namespace='payment')),

    # Coupons app URLs
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),

    # Rosetta translation interface
    path('rosetta/', include('rosetta.urls')),

    # Shop app (product listing, categories)
    path('', include('shop.urls', namespace='shop')),
)

# -----------------------------
# Serve media files in development
# -----------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
