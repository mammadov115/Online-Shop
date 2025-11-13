import redis
from django.conf import settings
from .models import Product

# connect to redis
# Establish a Redis connection using Django settings.
# This Redis instance is used for storing and retrieving product recommendation data.
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class Recommender:
    """
    A product recommendation system that uses Redis sorted sets to
    record and suggest products that are frequently bought together.

    Each product has an associated Redis key in the format:
    `product:<id>:purchased_with`

    Redis stores a sorted set (ZSET) of related product IDs with
    scores representing how often the products were bought together.
    """
    
    def get_product_key(self, id):
        """
        Returns the Redis key for the given product ID.
        Example: 'product:12:purchased_with'
        """
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
         """
        Updates the Redis store to record which products were bought together.

        Args:
            products (list[Product]): A list of Product instances that were purchased together.

        For each pair of products, it increments the association score
        in Redis using `ZINCRBY`.
        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    # Increment the score indicating how often two products are bought together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)
                
    def suggest_products_for(self, products, max_results=6):
        """
        Suggests related products based on previous purchase data.

        Args:
            products (list[Product]): The list of products a user has interacted with.
            max_results (int): The maximum number of suggested products to return.

        Returns:
            list[Product]: A list of suggested Product instances ordered by relevance.
        """
        product_ids = [p.id for p in products]
        # Case 1: Single product — fetch directly from its Redis key
        if len(products) == 1:
            # print(50*"-", "\n" ,r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_result] , "\n", 50*"-")
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # Case 2: Multiple products — combine their data into a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            # Merge all sorted sets for the given products
            r.zunionstore(tmp_key, keys)
            
            # Remove the original products from the recommendations
            r.rem(tmp_key, *product_ids)

            # Fetch the top related products
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result]

            # Clean up the temporary key
            r.delete(tmp_key)

        # Convert Redis byte strings to integers
        suggested_products_ids = [int(id) for id in suggestions]

        # Retrieve actual Product objects and sort them by Redis ranking
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products
    
    def clear_purchases(self):
        """
        Clears all purchase association data from Redis.

        This method removes all 'product:<id>:purchased_with' keys
        for every product in the database.
        """
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
