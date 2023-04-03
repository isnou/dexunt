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

    confirmed_orders = orders.filter(status='CONFIRMED').order_by('updated_at')
    processed_orders = orders.filter(status='PROCESSED').order_by('updated_at')
    packaged_orders = orders.filter(status='PACKAGED').order_by('updated_at')
    delivery_orders = orders.filter(status='DELIVERY').order_by('updated_at')

    return {
        'new_orders': new_orders,
        'confirmed_orders': confirmed_orders,
        'processed_orders': processed_orders,
        'packaged_orders': packaged_orders,
        'delivery_orders': delivery_orders,
    }




def confirmed(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'CONFIRMED'
            order.save()

def pending(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'NO-ANSWER'
            order.save()

def canceled(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'CANCELED'
            order.save()

def processed(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'PROCESSED'
            order.save()