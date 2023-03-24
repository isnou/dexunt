from .models import Cart, CartProduct, Product
from sell_manager.models import Province, Municipality

def details(request):
    url = "/main-shop/checkout-details.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    earned_points = 0
    province = None
    municipality = None

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)

        province = Province.objects.all().get(en_name=province_en_name)
        municipality = Municipality.objects.all().get(en_name=municipality_en_name)

    delivery_quotient = 0
    item_count = 0
    for product in cart.product.all():
        earned_points += product.points * product.quantity
        delivery_quotient += product.delivery * product.quantity
        item_count += product.quantity
    delivery_quotient = round(delivery_quotient / item_count)
    shipping_price = round((municipality.home_delivery_price * delivery_quotient) / 100)



    return {
        'shipping_price':shipping_price,
        'province':province,
        'municipality':municipality,
        'earned_points':earned_points,
        'url': url,
    }