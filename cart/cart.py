from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
#you try to get the cart from the current session
        cart = self.session.get(settings.CART_SESSION_ID) #store the current session to make it accessible to the other methods of the Cart class
# If no cart is present in the session, you create an empty cart by setting an empty dictionary in the session.
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
"""You will build your cart dictionary with product IDs as keys, and for each product
key, a dictionary will be a value that includes quantity and price.
guarantee that a product will not be added more than once to the cart.
This way, you can also simplify retrieving cart items"""
# --------------------------------------------------------------------
'''In the __iter__() method, you retrieve the Product instances that are present
in the cart to include them in the cart items. You copy the current cart in the cart
variable and add the Product instances to it. Finally, you iterate over the cart items,
converting each item's price back into decimal, and adding a total_price attribute
to each item. This __iter__() method will allow you to easily iterate over the items
in the cart in views and templates'''

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
# returning the number of total items stored in the cart
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
#1) product parameter: The product instance to add or update in the cart.
#2) quantity parameter: An optional integer with the product quantity. This defaults to 1.
#3) override_quantity parameter: This is a Boolean that indicates whether the quantity needs to be overridden with the given quantity (True), or whether the new
# quantity has to be added to the existing quantity (False).
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
# ----------------------------------------------------------
'''You use the product ID as a key in the cart's content dictionary. You convert the
product ID into a string because Django uses JSON to serialize session data, and
JSON only allows string key names. The product ID is the key, and the value
that you persist is a dictionary with quantity and price figures for the product'''
        product_id = str(product.id)
# The product's price is converted from decimal into a string in order to serialize it.
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
# call the save() method to save the cart in the session.
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
'''The save() method marks the session as modified using session.modified =
True. This tells Django that the session has changed and needs to be saved.'''

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
# calls the save() method to update the cart in the session.
            self.save()
# method to clear the cart session:
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
# calculate the total cost of the items in the cart:
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
