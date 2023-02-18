from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError


class ActiveManager(models.Manager):

    def isactive(self):
        return self.get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.PROTECT,
                            null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=False)
    objects = ActiveManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    objects = ActiveManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    objects = ActiveManager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):

    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line")
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True,)
    objects = ActiveManager()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Order must be unique for product")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image",
    )
    order = OrderField(unique_for_field="product_line", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_line.sku}_img"
