from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product, ProductLine


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)
