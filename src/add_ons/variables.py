
# -------------------------- carts ------------------------- #
def get_cart(request):
    from home.models import Cart, SelectedProduct

    if not request.user.is_authenticated:
        if not request.session.get('cart_ref', None):
            selected_cart = Cart()
            selected_cart.save_with_ref()
            request.session['cart_ref'] = selected_cart.ref
        else:
            ref = request.session.get('cart_ref')
            if Cart.objects.all().filter(ref=ref).exists():
                selected_cart = Cart.objects.all().get(ref=ref)
            else:
                selected_cart = Cart()
                selected_cart.save_with_ref()
                request.session['cart_ref'] = selected_cart.ref
    else:
        selected_cart = request.user.cart
    return selected_cart
#                                                            #
# ---------------------------------------------------------- #


# ------------------------ categories ---------------------- #
def categories():
    from management.models import Category

    activated = Category.objects.all().filter(is_activated=True)
    count = activated.count()

    best_rate = activated.first()
    for c in activated:
        if c.rates() > best_rate.rates():
            best_rate = c

    best_sale = activated.first()
    for c in activated:
        if c.sales() > best_sale.sales():
            best_sale = c


    values = {
        'activated': activated,
        'count': count,
        'best_rate': best_rate.collections.all().filter(is_activated=True)[:count],
        'best_sale': best_sale.collections.all().filter(is_activated=True)[:count],
    }
    return values
#                                                            #
# ---------------------------------------------------------- #