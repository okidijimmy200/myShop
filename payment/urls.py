from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'payment'

urlpatterns = [
    # url for The view that processes the payment
    path(_('process/'), views.payment_process, name='process'),
    # url for  view to redirect the user if the payment is successful
    path(_('done/'), views.payment_done, name='done'),
    # url for view to redirect the user if the payment is not successful
    path(_('canceled/'), views.payment_canceled, name='canceled'),
]
