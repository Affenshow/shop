from django.contrib import admin
from .models import Products, ProductsCategory, Basket, ProductRating, Order, OrderItem, Discount

admin.site.register(Products)
admin.site.register(ProductsCategory)
admin.site.register(Basket)
admin.site.register(ProductRating)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)