from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    """
    Model representing a discount coupon for the shop.

    Fields:
        code (str): Unique coupon code used by customers.
        valid_from (datetime): Start date/time from which the coupon is valid.
        valid_to (datetime): Expiration date/time of the coupon.
        discount (int): Discount percentage (0 to 100) applied to orders.
        active (bool): Whether the coupon is currently active.

    Usage:
        - Can be applied during checkout to reduce the order total.
        - Validation of active status and valid date range should be handled in forms/views.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique code customers enter to get a discount"
    )
    valid_from = models.DateTimeField(help_text="Start date/time of coupon validity")
    valid_to = models.DateTimeField(help_text="End date/time of coupon validity")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentage value (0 to 100)'
    )
    active = models.BooleanField(default=True, help_text="Indicates whether the coupon is currently active")

    def __str__(self):
        """
        String representation of the Coupon object.
        Returns the coupon code.
        """
        return self.code
