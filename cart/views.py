from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

# view for adding products to the cart or updating quantities for existing products.
@require_POST #require_POST decorator to allow only POST requests.
# The view receives the product ID as a parameter.
def cart_add(request, product_id):
    cart = Cart(request)
# retrieve the Product instance with the given ID
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
# validate CartAddProductForm. If the form is valid, you either add or update the product in the cart
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
# view redirects to the cart_detail URL
    return redirect('cart:cart_detail')

# view to remove items from cart
@require_POST #You use the require_POST decorator to allow only POST requests.
# The cart_remove view receives the product ID as a parameter.
def cart_remove(request, product_id):
    cart = Cart(request)
# retrieve the Product instance with the given ID and remove the product from the cart
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
# redirect the user to the cart_detail URL
    return redirect('cart:cart_detail')

# view to display the current cart and its items.
def cart_detail(request):
    cart = Cart(request)
# create an instance of CartAddProductForm for each item in the cart to allow
# changing product quantities.
    for item in cart:
# You initialize the form with the current item quantity and set the override field to True so that when you submit the form to the cart_
# add view, the current quantity is replaced with the new one.
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
        coupon_apply_form = CouponApplyForm()
        
        r = Recommender()
        cart_products = [item['product'] for item in cart]
        recommended_products = r.suggest_products_for(cart_products,
        max_results=4)
    return render(request, 'cart/detail.html',
                   {'cart': cart,
                    'coupon_apply_form': coupon_apply_form,
                    'recommended_products': recommended_products}
                   )
