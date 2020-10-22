from decimal import Decimal
from django.db import models
from shop.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from django.utils.translation import gettext_lazy as _

# The Order model contains several fields to store customer information and a paid Boolean field,
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
#  Every time an order is created in Braintree, a unique transaction identifier is generated. You will add a new field to the Order model of the orders application
# to store the transaction ID. This will allow you to link each order with its related Braintree transaction
    braintree_id = models.CharField(max_length=150, blank=True)
    # coupon & discount fields allow you to store an optional coupon for the order and the discount percentage applied with the coupon.
# The discount is stored in the related Coupon object, but you include it in the Order model to preserve it if the coupon is modified or deleted.
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
# You set on_delete to models.SET_NULL so that if the coupon gets deleted, the coupon field is set to Null, but the discount is preserved.
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'
# get_total_cost() method to obtain the total cost of the items bought in this order
    def get_total_cost(self):
        #get_total_cost will now take into account the discount applied,
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * \
            (self.discount / Decimal(100))

# The OrderItem model allows you to store the product, quantity, and price paid for each item.
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
# get_cost() to return the cost of the item
    def get_cost(self):
        return self.price * self.quantity
