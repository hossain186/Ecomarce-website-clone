from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Cart, Cart_Item
from product.models import Product

def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request, product_id):

    if request.method == 'POST':
        color = request.POST['COLOR']
        size = request.POST['SIZE']

        print(color, size)
    


    product = get_object_or_404(Product, id = product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))

    cart.save()


    try :
        cart_item = Cart_Item.objects.get(product= product, cart = cart)
        cart_item.quantity +=1
    except Cart_Item.DoesNotExist:

        cart_item = Cart_Item.objects.create(product = product, cart = cart, quantity= 1)

    cart_item.save()
    return redirect("cart")




def cart(request, total= 0,all_price=0, tax=0, quantity= 0, total_cart_item=0):

    try:
        cart_items = Cart_Item.objects.all()

        for item in cart_items:
            total += item.product.price* item.quantity
            quantity +=item.quantity
            tax += int(total*.02)
            all_price += total+tax
            total_cart_item += item.quantity


    except Exception:
        pass




    context = {'cart_items': cart_items, "total":total, "tax": tax, "all_price": all_price , "total_cart_item": total_cart_item}
    
    return render(request, 'cart/cart.html', context)




def remove_item(request,  product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = Cart_Item.objects.get(product = product, cart = cart)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()

    else:
        cart_item.delete()


    return redirect("cart")

def remove_cart(request, product_id):

    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = Cart_Item.objects.get(product = product, cart = cart)

    cart_item.delete()
    return redirect("cart")