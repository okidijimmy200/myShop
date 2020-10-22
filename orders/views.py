import weasyprint
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
# In the order_create view, you obtain the current cart from the session with  cart = Cart(request)
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
# You avoid saving it to the database yet by using commit=False.
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
# you create an Order object using the save() method of the OrderCreateForm form.
            """If the cart contains a coupon, you store the related coupon and the
discount that was applied. Then, you save the order object to the database."""
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id) #You call the delay() method of the task to execute it asynchronously.
             # set the order in the session
# -------------------------------------------------------------------------------
#after successfully creating an order, you set the order ID in the current session using the order_id session key.
            request.session['order_id'] = order.id
            # redirect for payment
# --------------------------------------------------------------------------------
# redirect the user to the payment:process URL,
            return redirect(reverse('payment:process'))
# NB: you need to run Celery in order for the order_created task to be queued and executed.
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

# staff_member_required decorator checks that both the is_active and is_ staff fields of the user requesting the page are set to True.
@staff_member_required
# you get the Order object with the given ID and render a template to display the order.
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
  
# staff_member_required decorator to make sure only staff users can access this view.
@staff_member_required
# view to generate a PDF invoice for an order.
def admin_order_pdf(request, order_id):
    # You get the Order object with the given ID
    order = get_object_or_404(Order, id=order_id)
# use the render_to_string() function provided by Django to render orders/order/pdf.html.
# The rendered HTML is saved in the html variable.
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
# you generate a new HttpResponse object specifying the application/ pdf content type
    response = HttpResponse(content_type='application/pdf')
# the Content-Disposition header to specify the filename
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
# WeasyPrint to generate a PDF file from the rendered HTML code and write the file to the HttpResponse object.
    weasyprint.HTML(string=html).write_pdf(response,
# You use the static file css/pdf.css to add CSS styles to the generated PDF file. Then, you load it from the local path by using the STATIC_ROOT setting.
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
# you return the generated response.
    return response
