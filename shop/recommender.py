import redis
from django.conf import settings
from .models import Product


# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

'''This is the Recommender class that will allow you to store product purchases and
retrieve product suggestions for a given product or products'''

class Recommender(object):
# The get_product_key() method receives an ID of a Product object and builds the Redis key for the sorted set where related products are stored, which looks like
# product id purchased_with.
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

# The products_bought() method receives a list of Product objects that have been bought together (that is, belong to the same order).
    def products_bought(self, products):
# You get the product IDs for the given Product objects.
        product_ids = [p.id for p in products]
# You iterate over the product IDs. For each ID, you iterate again over the product IDs and skip the same product so that you get the products that are bought together with each product.
        for product_id in product_ids:
            for with_id in product_ids:
# You get the Redis product key for each product bought using the get_product_id() method. For a product with an ID of 33, this method returns
# the key product:33:purchased_with. This is the key for the sorted set that contains the product IDs of products that were bought together with this one.
                # get the other products bought with each product
                if product_id != with_id:
# You increment the score of each product ID contained in the sorted set by 1. The score represents the times another product has been bought together
# with the given product
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id),
                              1,
                              with_id)

# method to retrieve the products that were bought together for a list of given products
    def suggest_products_for(self, products, max_results=6):
        # You get the product IDs for the given Product objects.
        product_ids = [p.id for p in products]
# If only one product is given, you retrieve the ID of the products that were bought together with the given product, ordered by the total number of times
# that they were bought together. To do so, you use Redis' ZRANGE command. You limit the number of results to the number specified in the max_results attribute (6 by default).
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
# products: This is a list of Product objects to get recommendations for. It can contain one or more products
                             self.get_product_key(product_ids[0]),
# max_results: This is an integer that represents the maximum number of recommendations to return.
                             0, -1, desc=True)[:max_results]
# If more than one product is given, you generate a temporary Redis key built with the IDs of the products
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
# You combine and sum all scores for the items contained in the sorted set of each of the given products. This is done using the Redis ZUNIONSTORE
# command. The ZUNIONSTORE command performs a union of the sorted sets with the given keys, and stores the aggregated sum of scores of the elements in a new Redis key.
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
# Since you are aggregating scores, you might obtain the same products you are getting recommendations for. You remove them from the generated sorted set using the ZREM command.
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
# You retrieve the IDs of the products from the temporary key, ordered by their score using the ZRANGE command. You limit the number of results to
# the number specified in the max_results attribute. Then, you remove the temporary key
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
# you get the Product objects with the given IDs and you order the products in the same order as them
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products
# method to clear the recommendations
    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
