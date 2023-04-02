from .models import Cart
from sell_manager.models import Order


def regular(request):
    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    processing_order = 'TO-DO'
    quality_check = 'TO-DO'
    packaging = 'TO-DO'
    on_delivery = 'TO-DO'

    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
        else:
            order = None
        # -- states :  UNCONFIRMED - CONFIRMED - NO-ANSWER - NO-NETWORK -( CANCELED )- PROCESSING - PACKAGING -
        # DELIVERY -( PENDING )-( PAID )-( REFUND )
        if order.status == 'UNCONFIRMED' or order.status == 'CONFIRMED':
            processing_order = 'IN-PROGRESS'

        if order.status == 'PROCESSING':
            processing_order = 'DONE'
            quality_check = 'IN-PROGRESS'

        if order.status == 'PACKAGING':
            processing_order = 'DONE'
            quality_check = 'DONE'
            packaging = 'IN-PROGRESS'

        if order.status == 'DELIVERY':
            processing_order = 'DONE'
            quality_check = 'DONE'
            packaging = 'DONE'
            on_delivery = 'IN-PROGRESS'

        context = {
            'order': order,
            'cart': cart,
            'processing_order': processing_order,
            'quality_check': quality_check,
            'packaging': packaging,
            'on_delivery': on_delivery,
        }

        return {
            'context': context,
        }