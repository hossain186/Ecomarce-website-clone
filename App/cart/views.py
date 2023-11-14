from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Cart, Cart_Item
from product.models import Product, Variation

def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    product_variation = []
    if request.method == 'POST':
        
        for item in request.POST:

            key = item 
            value = request.POST[key]


            try:
                variation = Variation.objects.get(product = product, variation_category__iexact = key, variation_value__iexact = value)
                product_variation.append(variation)

            except:
                pass 




   

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))

    cart.save()

    is_cartitem_exist = Cart_Item.objects.filter(product = product, cart= cart).exists()


    if is_cartitem_exist :
        
        cart_item = Cart_Item.objects.filter(product= product, cart = cart)
        #existing variation ,  
        # current_variation
        #cart_id
        ex_var_list = []
        id = []

        for item in  cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

            

        if product_variation in ex_var_list:
            idx = ex_var_list.index(product_variation)
            item_id = id[idx]
            item = Cart_Item.objects.get(product = product, id = item_id)
            item.quantity +=1
            item.save()
        else:
            item  = Cart_Item.objects.create(product = product, cart = cart ,quantity = 1)

            if len(product_variation)>0:
            
                item.variation.clear()

                
                item.variation.add(*product_variation)

            item.save()
        #cart_item.quantity +=1
    else:


        cart_item = Cart_Item.objects.create(product = product, cart = cart, quantity= 1)
        
        if len(product_variation)>0:
            cart_item.variation.clear()

            
            cart_item.variation.add(*product_variation)

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




def remove_item(request,  product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    

    try:
        cart_item = Cart_Item.objects.get(product = product, cart = cart, id = cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()

        else:
            cart_item.delete()
    except:
        pass


    return redirect("cart")

def remove_cart(request, product_id, cart_item_id):

    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = Cart_Item.objects.get(product = product, cart = cart, id = cart_item_id)

    cart_item.delete()
    return redirect("cart")
