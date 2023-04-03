from .models import Cart
from sell_manager.models import Order


def all_orders():
    try:
        orders = Order.objects.all()
    except Order.DoesNotExist:
        raise Http404("No orders")

    new_orders = orders \
        .exclude(status='CONFIRMED') \
        .exclude(status='CANCELED') \
        .exclude(status='PROCESSING') \
        .exclude(status='PACKAGING') \
        .exclude(status='DELIVERY') \
        .exclude(status='PENDING') \
        .exclude(status='PAID') \
        .exclude(status='REFUND') \
        .order_by('-created_at')

    return {
        'new_orders': new_orders,
    }




def confirm(request):
    orders = Order.objects.all()

    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if orders.filter(order_ref=order_ref).exists():
            order = orders.get(order_ref=order_ref)
            order.status = 'CONFIRMED'
            order.save()

def pend(request):
    orders = Order.objects.all()

    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if orders.filter(order_ref=order_ref).exists():
            order = orders.get(order_ref=order_ref)
            order.status = 'NO-ANSWER'
            order.save()

def cancel(request):
    orders = Order.objects.all()

    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if orders.filter(order_ref=order_ref).exists():
            order = orders.get(order_ref=order_ref)
            order.status = 'CANCELED'
            order.save()