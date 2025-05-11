from django.contrib import admin
from .models import Supplier, Buyer,  Product, Order

admin.site.register(Supplier)
admin.site.register(Buyer)
admin.site.register(Product)
admin.site.register(Order)
