from django.urls import path
from payment.views import (payment_canceled, payment_completed,
                           payment_process)
from payment.application.webhooks import stripe_webhook


app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='process'),
    path('completed/', payment_completed, name='completed'),
    path('canceled/', payment_canceled, name='canceled'),
    path('webhool/', stripe_webhook, name='stripe-webhook'),
]