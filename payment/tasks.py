from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@task
# You define the payment_completed task by using the @task decorator.
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    """
    In this task,
you use the EmailMessage class provided by Django to create an email object.
    """
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    # generate PDF
# you render the template into the html variable.
    html = render_to_string('orders/order/pdf.html', {'order': order})
# You generate the PDF file from the rendered template and output it to a BytesIO instance, which is an in-memory bytes buffer.
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    # attach PDF file
# you attach the generated PDF file to the EmailMessage object using the attach() method, including the contents of the out buffer.
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()
