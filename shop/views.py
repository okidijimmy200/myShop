from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
# you filter the QuerySet with available=True to retrieve only available products.
    products = Product.objects.filter(available=True)
    if category_slug:
# optional category_slug parameter to optionally filter products by a given category.
        # category = get_object_or_404(Category, slug=category_slug)
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

'''The product_detail view expects the id and slug parameters in order to
retrieve the Product instance wch can be got get this instance just through the ID,
since it's a unique attribute.'''
def product_detail(request, id, slug):
# the slug in the URL to build SEO-friendly URLs for products.
    # product = get_object_or_404(Product,
    #                             id=id,
    #                             slug=slug,
    #                             available=True)
    # adapted to retrieveobjects using translated fields.
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products
                   })
