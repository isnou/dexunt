from .models import Cart, CartProduct, Product
from sell_manager.models import Province, Municipality

def details(request):
    url = "/main-shop/checkout-details.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    earned_points = 0
    shipping_price = 0
    province = None
    municipality = None

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_price = request.POST.get('shipping_price', False)

        province = Province.objects.all().get(en_name=province_en_name)
        municipality = Municipality.objects.all().get(en_name=municipality_en_name)

    for product in cart.product.all():
        earned_points += product.points * product.quantity

    shipping_price = int(shipping_price)
    total_price = cart.sub_total_price + shipping_price

    context = {
        'cart': cart,
        'earned_points': earned_points,
        'shipping_price': shipping_price,
        'province': province,
        'municipality': municipality,
        'total_price': total_price,
    }

    return {
        'context':context,
        'url': url,
    }

def review(request):
    url = "/main-shop/checkout-review.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_price = request.POST.get('shipping_price', False)
        total_price = request.POST.get('total_price', False)
        earned_points = request.POST.get('earned_points', False)
        client_name = request.POST.get('client_name', False)
        phone_number = request.POST.get('phone_number', False)

        context = {
            'cart': cart,
            'province_en_name': province_en_name,
            'municipality_en_name': municipality_en_name,
            'client_name': client_name,
            'phone_number': phone_number,

            'earned_points': earned_points,
            'shipping_price': shipping_price,
            'total_price': total_price,
        }
    else:
        context = False

    return {
        'context':context,
        'url': url,
    }

def get_shipping_prices(request ,municipality_en_name):
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    municipality = Municipality.objects.all().get(en_name=municipality_en_name)

    delivery_quotients = 0
    for product in cart.product.all():
        delivery_quotients += product.delivery

    delivery_quotient = round(delivery_quotients / cart.product.all().count())
    home_delivery_price = round((municipality.home_delivery_price * delivery_quotient) / 100)
    desk_delivery_price = round((municipality.desk_delivery_price * delivery_quotient) / 100)

    sub_context = {
        'home_delivery_price': home_delivery_price,
        'desk_delivery_price': desk_delivery_price,
        'municipality': municipality,
    }

    return {
        'sub_context':sub_context,
    }


