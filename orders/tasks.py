from celery import task
from django.core.mail import send_mail
from .models import Order

# This is the place where Celery will look for asynchronous tasks.
# You define the order_created task by using the task decorator.
@task
# task. Your task function receives an order_id parameter. It's always recommended to only pass IDs to task functions and lookup objects when the task is executed.
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
# send_mail() function provided by Django to send an email notification to the user who placed the order.
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent
