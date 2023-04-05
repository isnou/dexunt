from sell_manager.models import Order, Cart
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

    pended_orders = orders.filter(status='CONFIRMED').order_by('updated_at')

    return {
        'pended_orders': pended_orders,
    }