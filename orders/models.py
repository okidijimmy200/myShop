from django.db import models
from shop.models import Product

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

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'
# get_total_cost() method to obtain the total cost of the items bought in this order
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

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
