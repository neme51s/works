from django.contrib import admin
from django.urls import reverse
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from order.export_to_csv import export_to_csv


def order_pdf(obj):
    url = reverse('order:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


def order_stripe_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_stripe_payment.short_description = 'Stripe payment'


class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 
                    'postal_code', 'city', order_stripe_payment, order_pdf, 'paid', 'created', 'updated'] 
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]