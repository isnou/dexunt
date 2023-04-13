from .models import Cart, CartProduct, Product, Coupon
from sell_manager.models import Province, Municipality, Order
from add_ons import functions


def regular(request):
    if not request.user.is_authenticated:
        cart = Cart.objects.all().get(ref=request.session.get('cart'))
    else:
        cart = request.user.cart.all()[:1].get()
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

        if shipping_type == 'home_delivery_price':
            shipping_type = 'TO-HOME'

        if shipping_type == 'desk_delivery_price':
            shipping_type = 'TO-DESK'

        if not request.user.is_authenticated:
            new_order = Order(cart_ref=cart.ref,
                              order_ref=order_ref,
                              device=cart.device,
                              operating_system=cart.operating_system,
                              ip_address=cart.ip_address,
                              client_name=client_name,
                              client_phone=phone_number,
                              province=province_en_name,
                              municipality=municipality_en_name,
                              shipping_type=shipping_type,
                              sub_total_price=cart.sub_total_price,
                              shipping_price=shipping_price,
                              )
        else:
            new_order = Order(order_ref=order_ref,
                              client_name=client_name,
                              client_phone=phone_number,
                              province=province_en_name,
                              municipality=municipality_en_name,
                              shipping_type=shipping_type,
                              sub_total_price=cart.sub_total_price,
                              shipping_price=shipping_price,
                              registred=True,
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
            if request.user.is_authenticated:
                if product.size_sku == 'main':
                    selected_product = request.user.booked.all().get(product_sku=product.product_sku)
                    selected_product.delete()
                else:
                    selected_product = user.booked.all().get(size_sku=product.size_sku)
                    selected_product.delete()

        cart.delete()

        if request.user.is_authenticated:
            request.user.order.add(new_order)


        context = {
            'new_order': new_order,
        }

        return {
            'context': context,
        }
