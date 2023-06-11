from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "location", "city", "zipcode", "district"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "selling_price",
        "discount_price",
        "description",
        "brand",
        "category",
        "product_image",
    ]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ("user", "customer", 'customer_info', "product", "product_info", "quantity", "ordered_date", "status")
    
    def customer_info(self, obj):
        link = reverse('admin:app_customer_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    def product_info(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

