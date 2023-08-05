from django.urls import path
from order.views import order_create, admin_order_pdf


app_name = 'order'

urlpatterns = [
    path('admin/order/<int:order_id>/pdf/',
         admin_order_pdf, name='admin_order_pdf'),
    path('create/', order_create, name='order_create'),
]