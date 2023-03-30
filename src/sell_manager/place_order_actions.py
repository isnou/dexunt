from .models import Cart, CartProduct, Product, Coupon
from sell_manager.models import Province, Municipality, Order
from add_ons import functions

def regular(request):
    url = "/main-shop/checkout-complete.html"
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    order_ref = functions.serial_number_generator(12).upper()
    new_order = Order(cart_ref = cart.ref,
                      order_ref = order_ref,
                      )
    new_order.save()

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_type = request.POST.get('shipping_type', False)
        client_name = request.POST.get('client_name', False)
        phone_number = request.POST.get('phone_number', False)
        coupon_code = request.POST.get('coupon_code', False)


    context = {

    }

    return {
        'context':context,
        'url': url,
    }

# ------------ order ------------
# cart_ref
# order_ref
# order_type
# created_at
# updated_at
# device
# operating_system
# ip_address
# state
# product
# client_name
# client_phone
# province
# municipality
# shipping_price
# coupon_code
# coupon_value
# coupon_type
# total_price
# additional_information
# gift_packaging
# theme
# occasion
# secured
# receiver_name
# receiver_message
