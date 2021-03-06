
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# language prefix to your URL patterns.
urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    #this pattern shd be above shop.urls bse its more restrictive
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls',namespace='orders')), #shd b before shop
    path(_('payment/'), include('payment.urls', namespace='payment')), #shd b before shop
    path(_('coupons/'), include('coupons.urls', namespace='coupons')), #shd b before shop
    path('rosetta/', include('rosetta.urls')), #shd be b4 shop
# URLs for the shop application under a custom namespace named shop.
    path('', include('shop.urls', namespace='shop')),

)

# serve uploaded image files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
'''
NB: In prod, never serve static files with django
'''