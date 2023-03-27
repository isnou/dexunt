from .models import Cart, CartProduct, Product
from shop_manager.models import Size, ShowcaseProduct
from sell_manager.models import Province


def add_product_to_cart(request):
    url = "/main-shop/main-page.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    redirecting = False
    provinces = False

    if request.method == 'POST':
        product_sku = request.POST.get('product_sku', False)
        variant_sku = request.POST.get('variant_sku', False)
        size_sku = request.POST.get('size_sku', False)
        change_url = request.POST.get('change_url', False)
        if change_url == 'go_to_cart':
            redirecting = True
            url = "/main-shop/shop-cart.html"
            try:
                provinces = Province.objects.all()
            except Province.objects.all().DoesNotExist:
                raise Http404("No provinces")

        selected_variant = ShowcaseProduct.objects.all().get(sku=variant_sku)
        selected_product = Product.objects.all().get(sku=product_sku)
        if not size_sku == 'main':
            selected_size = Size.objects.all().get(sku=size_sku)
            if selected_size.discount_price:
                price = selected_size.discount_price
            else:
                price = selected_size.sell_price
            en_detail = selected_size.en_title
            fr_detail = selected_size.fr_title
            ar_detail = selected_size.ar_title
            if selected_size.show_thumb:
                thumb = selected_size.thumb
            else:
                thumb = selected_product.album.all()[:1].get().image
        else:
            if selected_product.discount_price:
                price = selected_product.discount_price
            else:
                price = selected_product.sell_price
            en_detail = None
            fr_detail = None
            ar_detail = None
            thumb = selected_product.album.all()[:1].get().image

        delivery = selected_variant.delivery_quotient
        points = selected_variant.points
        en_name = selected_product.en_title
        fr_name = selected_product.fr_title
        ar_name = selected_product.ar_title
        en_spec = selected_product.en_spec
        fr_spec = selected_product.fr_spec
        ar_spec = selected_product.ar_spec

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
                    cart_product = CartProduct(delivery=delivery,
                                               points=points,
                                               en_name=en_name,
                                               fr_name=fr_name,
                                               ar_name=ar_name,

                                               en_spec=en_spec,
                                               fr_spec=fr_spec,
                                               ar_spec=ar_spec,

                                               en_detail=en_detail,
                                               fr_detail=fr_detail,
                                               ar_detail=ar_detail,

                                               thumb=thumb,

                                               product_sku=product_sku,
                                               size_sku=size_sku,
                                               quantity=int(quantity),
                                               price=price
                                               )
                    cart_product.save()
                    cart.product.add(cart_product)
        else:
            cart_product = CartProduct(delivery=delivery,
                                       points=points,
                                       en_name=en_name,
                                       fr_name=fr_name,
                                       ar_name=ar_name,

                                       en_spec=en_spec,
                                       fr_spec=fr_spec,
                                       ar_spec=ar_spec,

                                       en_detail=en_detail,
                                       fr_detail=fr_detail,
                                       ar_detail=ar_detail,

                                       thumb=thumb,

                                       product_sku=product_sku,
                                       size_sku=size_sku,
                                       quantity=int(quantity),
                                       price=price
                                       )
            cart_product.save()
            cart.product.add(cart_product)

    sub_total_price=0
    for cart_product in cart.product.all():
        sub_total_price += cart_product.price * cart_product.quantity
    cart.sub_total_price = sub_total_price
    cart.save()

    context = {
        'provinces': provinces,
        'redirecting': redirecting,
    }

    return {
        'url': url,
        'context': context,
    }

def show_cart():
    url = "/main-shop/shop-cart.html"

    try:
        provinces = Province.objects.all()
    except Province.objects.all().DoesNotExist:
        raise Http404("No provinces")

    return {
        'url': url,
        'provinces': provinces,
    }

def remove_product_from_cart(request):
    url = "/main-shop/main-page.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':
        size_sku = request.POST.get('size_sku', False)
        product_sku = request.POST.get('product_sku', False)

        if size_sku == 'main':
            selected_product = cart.product.all().get(product_sku=product_sku)
            if selected_product.quantity == 1:
                selected_product.delete()
            else:
                selected_product.quantity -= 1
                selected_product.save()
        else:
            selected_product = cart.product.all().get(size_sku=size_sku)
            if selected_product.quantity == 1:
                selected_product.delete()
            else:
                selected_product.quantity -= 1
                selected_product.save()

    sub_total_price = 0
    for cart_product in cart.product.all():
        sub_total_price += cart_product.price * cart_product.quantity
    cart.sub_total_price = sub_total_price
    cart.save()

    return {
        'url': url,
    }

def remove_quantity(request):
    url = "/main-shop/shop-cart.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':
        size_sku = request.POST.get('size_sku', False)
        product_sku = request.POST.get('product_sku', False)

        if size_sku == 'main':
            selected_product = cart.product.all().get(product_sku=product_sku)
            if selected_product.quantity == 1:
                selected_product.delete()
            else:
                selected_product.quantity -= 1
                selected_product.save()
        else:
            selected_product = cart.product.all().get(size_sku=size_sku)
            if selected_product.quantity == 1:
                selected_product.delete()
            else:
                selected_product.quantity -= 1
                selected_product.save()

    sub_total_price = 0
    for cart_product in cart.product.all():
        sub_total_price += cart_product.price * cart_product.quantity
    cart.sub_total_price = sub_total_price
    cart.save()

    return {
        'url': url,
    }