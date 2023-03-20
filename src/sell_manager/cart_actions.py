from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Cart, CartProduct, Product


def add_product_to_cart(request):
    url = "/main-shop/main-page.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':

        size_sku = request.POST.get('size_sku', False)
        product_sku = request.POST.get('product_sku', False)
        quantity = request.POST.get('quantity', False)

        if cart.product.all().filter(product_sku=product_sku).exists():
            if size_sku == 'main':
                cart_product = cart.product.all().get(product_sku=product_sku)
                cart_product.quantity = quantity
                cart_product.save()
            else:
                if cart.product.all().filter(size_sku=size_sku).exists():
                    cart_product = cart.product.all().get(size_sku=size_sku)
                    cart_product.quantity = quantity
                    cart_product.save()
                else:
                    cart_product = CartProduct(product_sku=product_sku,
                                               size_sku=size_sku,
                                               quantity=int(quantity),
                                               )
                    cart_product.save()
                    cart.product.add(cart_product)
        else:
            cart_product = CartProduct(product_sku=product_sku,
                                       size_sku=size_sku,
                                       quantity=int(quantity),
                                       )
            cart_product.save()
            cart.product.add(cart_product)



    return {
        'url': url,
    }