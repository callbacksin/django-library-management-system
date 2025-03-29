from django.contrib import admin

from .models import OrderBook, Order

admin.site.register(OrderBook)
admin.site.register(Order)
