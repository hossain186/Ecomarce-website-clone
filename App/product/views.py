from django.shortcuts import render, get_object_or_404, HttpResponse

from product.models import Product,Variation
from category.models import Category
from cart.models import Cart_Item
from cart.views import _cart_id
from django.core.paginator import EmptyPage , PageNotAnInteger, Paginator
from django.db.models import Q 



def store(request, category_slug= None):

    
    categories  = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories , is_available = True)
        
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paginate_product = paginator.get_page(page)
        paginate_product_count = products.count()

    else:


        products = Product.objects.all().filter(is_available = True)
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paginate_product = paginator.get_page(page)
        paginate_product_count = products.count()


    context = {"products": paginate_product, "product_count": paginate_product_count}


    return render(request, "product/store.html", context)


def product_detail(request, category_slug, product_slug):

    product = get_object_or_404(Product, category__slug = category_slug, slug = product_slug)

    

    

    in_cart = Cart_Item.objects.filter(cart__cart_id = _cart_id(request), product = product).exists()

    context = {"product": product, 'in_cart':in_cart}

    return render(request, "product/detail.html", context)


def search(request):

    if "keyword" in request.GET:

        keyword = request.GET["keyword"]

        if keyword:

            products =Product.objects.order_by("created_date").filter(Q(descriptions__icontains = keyword) | Q(product_name__icontains = keyword))


        context = {"products":products}

        return render(request,"product/store.html", context)




