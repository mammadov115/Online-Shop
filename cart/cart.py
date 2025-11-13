from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart:
    """
    A shopping cart class that manages the user's session-based cart.

    Features:
    - Add, remove, and iterate over products in the cart
    - Apply discounts using coupons
    - Compute total price and total price after discount
    - Supports quantity override and automatic session saving

    Session Keys:
        - CART_SESSION_ID: stores cart items as a dictionary
        - coupon_id: stores applied coupon ID
    """

    def __init__(self, request):
        """
        Initialize the cart with the current session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Create empty cart if it doesn't exist
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.

        Args:
            product (Product): Product instance to add
            quantity (int): Quantity to add
            override_quantity (bool): If True, replace current quantity
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it is saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.

        Args:
            product (Product): Product instance to remove
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and attach the Product instance.

        Yields:
            dict: Contains 'product', 'price', 'quantity', and 'total_price'
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        # Attach product instances to cart items
        for product in products:
            cart[str(product.id)]['product'] = product

        # Convert price to Decimal and compute total price per item
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart (sum of quantities).
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Compute total price of all items in the cart before discount.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """
        Get the currently applied coupon, if any.

        Returns:
            Coupon or None
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        Compute discount amount based on applied coupon.

        Returns:
            Decimal: Discount amount
        """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """
        Compute total price after applying coupon discount.

        Returns:
            Decimal: Total price after discount
        """
        return self.get_total_price() - self.get_discount()
