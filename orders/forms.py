from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField

class OrderCreateForm(forms.ModelForm):
    """
    Form for creating a new Order in the checkout process.

    Overrides the postal_code field to use a US-specific zip code validator.
    This ensures that users enter valid postal codes for US addresses.

    Fields included:
        - first_name
        - last_name
        - email
        - address
        - postal_code (validated as US ZIP code)
        - city
    """
    postal_code = USZipCodeField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        # You can add widgets, labels, or help_text here if needed for better UX.
