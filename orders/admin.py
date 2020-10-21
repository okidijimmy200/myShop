import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def export_to_csv(modeladmin, request, queryset):
# You create an instance of HttpResponse, specifying the text/csv content type, to tell the browser that the response has to be treated as a CSV file
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
# You also add a Content-Disposition header to indicate that the HTTP response contains an attached file.
    response['Content-Disposition'] = content_disposition
# You create a CSV writer object that will write to the response object.
    writer = csv.writer(response)
# You get the model fields dynamically using the get_fields() method of the model _meta options. You exclude many-to-many and one-to-many relationships
    fields = [field for field in opts.get_fields() if not field.many_to_many\
    and not field.one_to_many]
    # Write a first row with header information(You write a header row including the field names)
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
# You iterate over the given QuerySet and write a row for each object returned by the QuerySet. You take care of formatting datetime objects because the output value for CSV has to be a string.
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
# You customize the display name for the action in the actions dropdown element of the administration site by setting a short_description attribute on the function
export_to_csv.short_description = 'Export to CSV'

# link to each Order object
# This is a function that takes an Order object as an argument and returns an HTML link for the admin_order_detail URL
def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
# Django escapes HTML output by default. You have to use the mark_safe function to avoid auto-escaping.
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
# If you specify a short_description attribute for your callable, Django will use it for the name of the column
order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    # order_detail to display the link:
    list_filter = ['paid', 'created', 'updated']
# You use a ModelInline class for the OrderItem model to include it as an inline in the OrderAdmin class. An inline allows you to include a model on the same edit
# page as its related model
    inlines = [OrderItemInline]
    actions = [export_to_csv]
