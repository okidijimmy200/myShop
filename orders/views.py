from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
# In the order_create view, you obtain the current cart from the session with  cart = Cart(request)
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id) #You call the delay() method of the task to execute it asynchronously.
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
    
# NB
'''Depending on the request method, you perform
the following tasks:
• GET request: Instantiates the OrderCreateForm form and renders the
orders/order/create.html template.
• POST request: Validates the data sent in the request. If the data is valid,
you create a new order in the database using order = form.save(). You
iterate over the cart items and create an OrderItem for each of them. Finally,
you clear the cart's contents and render the template orders/order/
created.html.'''
