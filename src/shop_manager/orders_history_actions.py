from sell_manager.models import Order
from .models import Product, Size


def all_orders():
    try:
        orders = Order.objects.all()
    except Order.DoesNotExist:
        raise Http404("No orders")

    # ---------------- status -----------------
    # UNCONFIRMED - NO-ANSWER                --
    # CONFIRMED                              --
    # PROCESSED                              --
    # PACKAGED                               --
    # DELIVERED                              --
    # PAID                                   --
    # PENDED - REFUNDED - CANCELED           --
    # -----------------------------------------

    canceled_orders = orders.filter(status='CANCELED').order_by('updated_at')
    pended_orders = orders.filter(status='PENDED').order_by('updated_at')
    refunded_orders = orders.filter(status='REFUNDED').order_by('updated_at')

    return {
        'canceled_orders': canceled_orders,
        'pended_orders': pended_orders,
        'refunded_orders': refunded_orders,
    }