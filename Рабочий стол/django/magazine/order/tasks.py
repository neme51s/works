import requests

from celery import shared_task
from django.core.mail import send_mail
from .models import Order


token = '6292503156:AAE9JywTHj50KptcEPxyOtAtwnKTmzHAgBE'
chat_id = '-913101521'
apiURL = f'https://api.telegram.org/bot{token}/sendMessage'


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
        f'You have successfully placed an order.' \
        f'Your order ID is {order.id}.'
    mail_sent = send_mail(
        subject, message,
        'admin@myshop.com', [order.email]
    )
    try:
        requests.post(
            apiURL, json={
                'chat_id': chat_id,
                'text': f'Заказ № {order.id} был добавлен в Админ панель'})
    except Exception as e:
        print(e)

    return mail_sent


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
        f'You have successfully placed an order.' \
        f'Your order ID is {order.id}.'
    mail_sent = send_mail(
        subject, message,
        'admin@myshop.com', [order.email]
    )
    try:
        requests.post(
            apiURL, json={
                'chat_id': chat_id,
                'text': f'Заказ № {order.id} был добавлен в Админ панель'})
    except Exception as e:
        print(e)

    return mail_sent