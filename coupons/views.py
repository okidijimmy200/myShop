from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

# apply the require_POST decorator to this view to restrict it to POST requests.
@require_POST
# The coupon_apply view validates the coupon and stores it in the user's session.
def coupon_apply(request):
    """
    The coupon has to be currently active (active=True) and valid
for the current datetime. You use Django's timezone.now() function to get
the current timezone-aware datetime
    """
    now = timezone.now()
# instantiate the CouponApplyForm form using the posted data and check that the form is valid
    form = CouponApplyForm(request.POST)
# If the form is valid, you get the code entered by the user from the form's cleaned_data dictionary
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
# You try to retrieve the Coupon object with the given code. You use the iexact field lookup to perform a case-insensitive exact match.
            coupon = Coupon.objects.get(code__iexact=code,
# get the current timezone aware datetime and you compare it with the valid_from and valid_to fields performing lte (less than or equal to) and gte (greater than or equal to) field lookups, respectively.
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
# You store the coupon ID in the user's session.
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
# You redirect the user to the cart_detail URL to display the cart with the coupon applied.
    return redirect('cart:cart_detail')
