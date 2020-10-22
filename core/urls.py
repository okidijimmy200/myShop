
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #this pattern shd be above shop.urls bse its more restrictive
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls',namespace='orders')), #shd b before shop
    path('payment/', include('payment.urls', namespace='payment')), #shd b before shop
    path('coupons/', include('coupons.urls', namespace='coupons')), #shd b before shop
# URLs for the shop application under a custom namespace named shop.
    path('', include('shop.urls', namespace='shop')),

]

# serve uploaded image files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
'''
NB: In prod, never serve static files with django
'''