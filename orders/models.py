from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _

# Models for handling orders and order items in the e-commerce application.


class Order(models.Model):
    """
    Represents a customer order.

    Stores customer information, order status, applied coupon and discount,
    and provides methods to calculate total cost with or without discounts.
    """

    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("e-mail"))
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("postal code"), max_length=20)
    city = models.CharField(_("city"), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Applied coupon for this order, if any."
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount percentage applied to the order."
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        """
        Returns a string representation of the order.
        """
        return f'Order {self.id}'

    def get_total_cost(self):
        """
        Calculates the total cost after applying the discount.

        Returns:
            Decimal: Total order cost after discount.
        """
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_total_cost_before_discount(self):
        """
        Calculates the total cost of all order items before any discount.

        Returns:
            Decimal: Total cost of all items.
        """
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """
        Calculates the discount amount based on the order's discount percentage.

        Returns:
            Decimal: Discount amount to subtract from the total cost.
        """
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)


class OrderItem(models.Model):
    """
    Represents a single item in an order.

    Links a product to an order, storing the price at the time of purchase
    and the quantity ordered.
    """

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        help_text="The order this item belongs to."
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        help_text="The product that was ordered."
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per item at time of order.")
    quantity = models.PositiveIntegerField(default=1, help_text="Quantity of this product ordered.")

    def __str__(self):
        """
        Returns a string representation of the order item.
        """
        return str(self.id)

    def get_cost(self):
        """
        Calculates the total cost for this item (price * quantity).

        Returns:
            Decimal: Total cost for this order item.
        """
        return self.price * self.quantity
