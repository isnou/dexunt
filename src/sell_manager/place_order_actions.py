from .models import Cart, CartProduct, Product, Coupon
from sell_manager.models import Province, Municipality, Order
from add_ons import functions

def regular(request):
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    order_ref = functions.serial_number_generator(12).upper()

    if request.method == 'POST':
        province_en_name = request.POST.get('province_en_name', False)
        municipality_en_name = request.POST.get('municipality_en_name', False)
        shipping_type = request.POST.get('shipping_type', False)
        client_name = request.POST.get('client_name', False)
        phone_number = request.POST.get('phone_number', False)
        coupon_code = request.POST.get('coupon_code', False)

        municipality = Municipality.objects.all().get(en_name=municipality_en_name)
        shipping_price = functions.get_shipping_price(cart, municipality, shipping_type)

        new_order = Order(cart_ref=cart.ref,
                          order_ref=order_ref,
                          device=cart.device,
                          operating_system=cart.operating_system,
                          ip_address=cart.ip_address,
                          client_name=client_name,
                          client_phone=phone_number,
                          province=province_en_name,
                          municipality=municipality_en_name,
                          sub_total_price=cart.sub_total_price,
                          shipping_price=shipping_price,
                          )

        if Coupon.objects.all().filter(code=coupon_code).exists():
            coupon = Coupon.objects.all().get(code=coupon_code)
            total_price = cart.sub_total_price + shipping_price
            discounted_price = functions.validate_promotion(coupon_code, total_price)
            new_order.coupon_code = coupon_code
            new_order.coupon_type = coupon.coupon_type
            new_order.coupon_value = coupon.value
            new_order.final_price = discounted_price
        else:
            total_price = cart.sub_total_price + shipping_price
            new_order.final_price = total_price
        new_order.points = functions.get_earned_points(cart)

        new_order.save()

        for product in cart.product.all():
            new_order.product.add(product)

        cart.delete()

        context = {
            'new_order': new_order,
        }

        return {
            'context': context,
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

# sub_total_price
# shipping_price
# final_price


# additional_information
# gift_packaging
# theme
# occasion
# secured
# receiver_name
# receiver_message
