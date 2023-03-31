from sell_manager.models import Province, Municipality, Cart, CartProduct, Product, Coupon
import random
import string


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

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
        if coupon.quantity:
            if coupon.coupon_type == 'SUBTRACTION':
                discounted_price = total_price - coupon.value
            elif coupon.coupon_type == 'PERCENTAGE':
                discounted_price = total_price - round((total_price * coupon.value) / 10000) * 100
            else:
                discounted_price = None
        else:
            coupon = 'EXPIRED'
            discounted_price = None
    else:
        if coupon_code == 'INTRO_CODE':
            coupon = 'INTRO'
        else:
            coupon = 'WRONG'
        discounted_price = None

    return {
        'coupon': coupon,
        'discounted_price': discounted_price,
    }

def validate_promotion(coupon_code, total_price):
    if Coupon.objects.all().filter(code=coupon_code).exists():
        coupon = Coupon.objects.all().get(code=coupon_code)
        if coupon.quantity:
            if coupon.coupon_type == 'SUBTRACTION':
                discounted_price = total_price - coupon.value
                coupon.quantity -= 1
                coupon.save()
            elif coupon.coupon_type == 'PERCENTAGE':
                discounted_price = total_price - round((total_price * coupon.value) / 10000) * 100
                coupon.quantity -= 1
                coupon.save()
            else:
                discounted_price = None
        else:
            discounted_price = None
    else:
        discounted_price = None

    return discounted_price