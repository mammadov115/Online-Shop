from django import forms
from django.utils.translation import gettext_lazy as _

# Choices for quantity selection: 1 to 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    """
    Form for adding a product to the shopping cart.

    Fields:
        quantity (int): Number of items to add (1-20).
        override (bool): Whether to replace existing quantity or add to it.
                         This is handled via a hidden input in templates.

    Usage:
        - Rendered in product detail or cart templates.
        - Submits POST request to update the cart.
        - 'override' field allows templates to specify adding vs replacing quantity.
    """
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label=_('Quantity')
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
