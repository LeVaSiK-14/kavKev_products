from django.contrib import admin
from products.models import *

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(RaitingStar)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartProduct)
