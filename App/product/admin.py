from django.contrib import admin

# Register your models here.
from .models import Product, Variation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('product_name' , 'slug' , 'price', 'stock' , 'category', 'modified_date','is_available')
    prepopulated_fields = {'slug' : ['product_name'],}


@admin.register(Variation)
class variationManager(admin.ModelAdmin):
    list_display = ['product', "variation_category","variation_value", "is_active"]
    list_editable = ['is_active']
    list_filter = ['product', "variation_category","variation_value", "is_active"]