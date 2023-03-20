from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Cart, CartProduct, Product


def add_product_to_cart(request):
    url = "/main-shop/main-page.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':

        size_sku = request.POST.get('size_sku', False)
        product_sku = request.FILES.get('product_sku', False)
        quantity = request.POST.get('quantity', False)

        if not size_sku == 'main':
            size_sku = size_sku
        else:
            size_sku = None

        cart_product = CartProduct(product_sku=product_sku,
                                   size_sku=size_sku,
                                   quantity=quantity,
                                   )
        cart_product.save()
        cart.product.add(cart_product)



    return {
        'url': url,
    }