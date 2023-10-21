from django.contrib import admin

# Register your models here.
from .models import Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('product_name' , 'slug' , 'price', 'stock' , 'category', 'modified_date','is_available')
    prepopulated_fields = {'slug' : ['product_name'],}
