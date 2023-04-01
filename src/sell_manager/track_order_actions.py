from .models import Cart
from sell_manager.models import Order


def regular(request):
    cart = Cart.objects.all().get(ref=request.session.get('cart'))

    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
        else:
            order = None

        context = {
            'order': order,
            'cart': cart,
        }

        return {
            'context': context,
        }