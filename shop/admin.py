from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
# attribute to specify fields where the value is automatically set using the value of other fields.
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
# You use the list_editable attribute in the ProductAdmin class to set the fields that can be edited from the list display page of the administration site
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# This will allow you to edit multiple rows at once. Any field in list_editable must also be listed
# in the list_display attribute, since only the fields displayed can be edited.
    list_editable = ['price', 'available']
# attribute to specify fields where the value is automatically set using the value of other fields.
    prepopulated_fields = {'slug': ('name',)}