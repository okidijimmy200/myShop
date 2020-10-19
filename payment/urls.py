from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # url for The view that processes the payment
    path('process/', views.payment_process, name='process'),
    # url for  view to redirect the user if the payment is successful
    path('done/', views.payment_done, name='done'),
    # url for view to redirect the user if the payment is not successful
    path('canceled/', views.payment_canceled, name='canceled'),
]
