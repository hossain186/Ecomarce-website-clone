from .models import Cart , Cart_Item
from .views import _cart_id

def counter(request):

    if "admin" in request.path:
        return {}

    else:

        try:
            cart_count = 0
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            cart_items = Cart_Item.objects.all().filter(cart = cart[:1])

            for cart_item in cart_items:

                cart_count += cart_item.quantity

        except Cart.DoesNotExist:
            cart_item = 0
        
        return dict(cart_count = cart_count)