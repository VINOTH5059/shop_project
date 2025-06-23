from django.contrib import admin
from .models import *
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'description']
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'Product_image', 'description']
admin.site.register(Category,CategoryAdmin),
admin.site.register(Product,ProductAdmin)
