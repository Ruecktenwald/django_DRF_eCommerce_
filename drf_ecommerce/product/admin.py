from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
