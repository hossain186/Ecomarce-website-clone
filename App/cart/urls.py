from django.urls import path

from .views import *

urlpatterns = [
    path('', cart, name="cart"),
    path("<int:product_id>", add_cart, name="add_cart"),
    path("remove_cart_item/<int:product_id>/", remove_item, name="remove_item"),
    path("remove_cart/<int:product_id>/", remove_cart, name="remove_cart")
]