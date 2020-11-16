from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

'''The Category model now inherits from TranslatableModel instead of models.
Model and both the name and slug fields are included in the TranslatedFields
wrapper'''
class Category(TranslatableModel):
    # name field
    translations = TranslatedFields(
        name = models.CharField(max_length=200,
                                db_index=True),
        # unique slug field (unique implies the creation of an index
        slug = models.SlugField(max_length=200,
                                db_index=True,
                                unique=True)
    )
    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


'''add translations for the name, slug, and description
fields,'''
class Product(TranslatableModel):
    translations = TranslatedFields(
    # name
    name = models.CharField(max_length=200, db_index=True),
# slug: The slug for this product to build beautiful URLs.
    slug = models.SlugField(max_length=200, db_index=True),
# image: An optional product image.
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    )
    # category: A ForeignKey to the Category model. This is a one-to-many relationship: a product belongs to one category and a category contains
# multiple products.
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
# description: An optional description of the product.
    description = models.TextField(blank=True)
# price: This field uses Python's decimal.Decimal type to store a fixedprecision decimal number. The maximum number of digits (including
# the decimal places) is set using the max_digits attribute and decimal places with the decimal_places attribute
    price = models.DecimalField(max_digits=10, decimal_places=2)
# available: A Boolean value that indicates whether the product is available
# or not. It will be used to enable/disable the product in the catalog.
    available = models.BooleanField(default=True)
# created: This field stores when the object was created.
    created = models.DateTimeField(auto_now_add=True)
# updated: This field stores when the object was last updated.
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        '''The current version of django-parler does not provide support
to validate index_together'''
        # ordering = ('name',)
# index_together meta option to specify an index for the id and slug fields together
# You define this index because you plan to query products by both id and slug.
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
