from .models import Cart, CartProduct, Product, Coupon
from sell_manager.models import Province, Municipality

def details(request):
    url = "/main-shop/checkout-details.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    earned_points = 0
    shipping_price = 0
    province = None
    municipality = None
    shipping_type = None
    coupon_code = None

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_type = request.POST.get('shipping_type', False)
        coupon_code = request.POST.get('coupon_code', False)

        province = Province.objects.all().get(en_name=province_en_name)
        municipality = Municipality.objects.all().get(en_name=municipality_en_name)
        shipping_price = get_shipping_price(cart, municipality, shipping_type)


    for product in cart.product.all():
        earned_points += product.points * product.quantity

    total_price = cart.sub_total_price + shipping_price
    coupon = check_promotion(coupon_code, total_price).get('coupon')
    discounted_price = check_promotion(coupon_code, total_price).get('discounted_price')

    context = {
        'cart': cart,
        'earned_points': earned_points,
        'shipping_price': shipping_price,
        'province': province,
        'municipality': municipality,
        'total_price': total_price,

        'shipping_type': shipping_type,
        'coupon': coupon,
        'discounted_price': discounted_price,
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
    home_delivery_price = round((municipality.home_delivery_price * delivery_quotient) / 10000) * 100
    desk_delivery_price = round((municipality.desk_delivery_price * delivery_quotient) / 10000) * 100

    sub_context = {
        'home_delivery_price': home_delivery_price,
        'desk_delivery_price': desk_delivery_price,
        'municipality': municipality,
    }

    return {
        'sub_context':sub_context,
    }

def get_shipping_price(cart, municipality, shipping_type):

    delivery_quotients = 0
    for product in cart.product.all():
        delivery_quotients += product.delivery

    delivery_quotient = round(delivery_quotients / cart.product.all().count())
    home_delivery_price = round((municipality.home_delivery_price * delivery_quotient) / 10000) * 100
    desk_delivery_price = round((municipality.desk_delivery_price * delivery_quotient) / 10000) * 100

    if shipping_type == 'home_delivery_price':
        return home_delivery_price

    if shipping_type == 'desk_delivery_price':
        return desk_delivery_price

def check_promotion(coupon_code, total_price):
    if Coupon.objects.all().filter(code=coupon_code).exists():
        coupon = Coupon.objects.all().get(code=coupon_code)
        if coupon.coupon_type == 'SUBTRACTION':
            discounted_price = total_price - coupon.value
        elif coupon.coupon_type == 'PERCENTAGE':
            discounted_price = round((total_price * coupon.value) / 10000) * 100
        else:
            discounted_price = None
    else:
        coupon = None
        discounted_price = None

    return {
        'coupon': coupon,
        'discounted_price': discounted_price,
    }

