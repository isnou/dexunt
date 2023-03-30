from .models import Cart, CartProduct, Product, Coupon, Province, Municipality
from add_ons import functions

def details(request):
    url = "/main-shop/checkout-details.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    earned_points = 0

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_type = request.POST.get('shipping_type', False)
        coupon_code = request.POST.get('coupon_code', False)

        province = Province.objects.all().get(en_name=province_en_name)
        municipality = Municipality.objects.all().get(en_name=municipality_en_name)
        shipping_price = functions.get_shipping_price(cart, municipality, shipping_type)

        for product in cart.product.all():
            earned_points += product.points * product.quantity

        total_price = cart.sub_total_price + shipping_price
        coupon = functions.check_promotion(coupon_code, total_price).get('coupon')
        discounted_price = functions.check_promotion(coupon_code, total_price).get('discounted_price')

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
            'context': context,
            'url': url,
        }


def review(request):
    url = "/main-shop/checkout-review.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_price = request.POST.get('shipping_price', False)
        shipping_type = request.POST.get('shipping_type', False)
        total_price = request.POST.get('total_price', False)
        earned_points = request.POST.get('earned_points', False)
        client_name = request.POST.get('client_name', False)
        phone_number = request.POST.get('phone_number', False)
        coupon_code = request.POST.get('coupon_code', False)
        discounted_price = request.POST.get('discounted_price', False)

        coupon = functions.check_promotion(coupon_code, 0).get('coupon')

        context = {
            'cart': cart,
            'coupon': coupon,
            'province_en_name': province_en_name,
            'municipality_en_name': municipality_en_name,
            'shipping_type': shipping_type,
            'client_name': client_name,
            'phone_number': phone_number,

            'earned_points': earned_points,
            'shipping_price': shipping_price,
            'total_price': total_price,
            'discounted_price': discounted_price,
        }

        return {
            'context': context,
            'url': url,
        }


