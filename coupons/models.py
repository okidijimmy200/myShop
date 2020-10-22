from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


class Coupon(models.Model):
# code: The code that users have to enter in order to apply the coupon to their purchase.
    code = models.CharField(max_length=50,
                            unique=True)
# valid_from: The datetime value that indicates when the coupon becomes valid.
    valid_from = models.DateTimeField()
# valid_to: The datetime value that indicates when the coupon becomes invalid.
    valid_to = models.DateTimeField()
# discount: The discount rate to apply (this is a percentage, so it takes values from 0 to 100). You use validators for this field to limit the minimum and maximum accepted values.
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)])
# active: A Boolean that indicates whether the coupon is active.
    active = models.BooleanField()

    def __str__(self):
        return self.code
