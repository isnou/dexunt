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
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'CONFIRMED'
            order.save()

def pend(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'NO-ANSWER'
            order.save()

def cancel(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'CANCELED'
            order.save()