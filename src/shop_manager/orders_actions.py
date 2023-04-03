from sell_manager.models import Order, Cart


def all_orders():
    try:
        orders = Order.objects.all()
    except Order.DoesNotExist:
        raise Http404("No orders")

    # ------------- status -------------
    # UNCONFIRMED - NO-ANSWER         --
    # CONFIRMED                       --
    # PROCESSED                       --
    # PACKAGED                        --
    # DELIVERY                        --
    # PAID                            --
    # PENDING - REFUND - CANCELED     --
    # ----------------------------------

    new_orders = orders \
        .exclude(status='CONFIRMED') \
        .exclude(status='CANCELED') \
        .exclude(status='PROCESSED') \
        .exclude(status='PACKAGED') \
        .exclude(status='DELIVERY') \
        .exclude(status='PEND') \
        .exclude(status='PAID') \
        .exclude(status='REFUND') \
        .order_by('-created_at')

    confirmed = orders.filter(status='CONFIRMED')
    processed = orders.filter(status='PROCESSED')
    packaged = orders.filter(status='PACKAGED')
    delivery = orders.filter(status='DELIVERY')

    return {
        'new_orders': new_orders,
        'confirmed': confirmed,
        'processed': processed,
        'packaged': packaged,
        'delivery': delivery,
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