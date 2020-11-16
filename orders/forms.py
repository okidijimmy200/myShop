from django import forms
from .models import Order
#  add the United States' zip code field so that a valid United States zip code is required to create a new orde
from localflavor.us.forms import USZipCodeField

# a form to enter the order details
class OrderCreateForm(forms.ModelForm):
    postal_code = USZipCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
