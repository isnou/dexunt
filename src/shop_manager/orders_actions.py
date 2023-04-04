from sell_manager.models import Order, Cart
from .models import Product, Size


def all_orders():
    try:
        orders = Order.objects.all()
    except Order.DoesNotExist:
        raise Http404("No orders")

    for order in orders:
        for order_product in order.product.all():
            if order_product.size_sku == 'main':
                inventory_product = Product.objects.all().get(sku=order_product.product_sku)
                if inventory_product.quantity < order_product.quantity:
                    order_product.quantity_issue=True
                    order_product.save()
                    order.quantity_issue=True
                    order.save()
                else:
                    order_product.quantity_issue=False
                    order_product.save()
                    order.quantity_issue=False
                    order.save()
            else:
                inventory_product = Size.objects.all().get(sku=order_product.size_sku)
                if inventory_product.quantity < order_product.quantity:
                    order_product.quantity_issue=True
                    order_product.save()
                    order.quantity_issue=True
                    order.save()
                else:
                    order_product.quantity_issue=False
                    order_product.save()
                    order.quantity_issue=False
                    order.save()

    # ---------------- status -----------------
    # UNCONFIRMED - NO-ANSWER                --
    # CONFIRMED                              --
    # PROCESSED                              --
    # PACKAGED                               --
    # DELIVERED                              --
    # PAID                                   --
    # PENDED - REFUNDED - CANCELED           --
    # -----------------------------------------

    new_orders = orders \
        .exclude(status='CONFIRMED') \
        .exclude(status='CANCELED') \
        .exclude(status='PROCESSED') \
        .exclude(status='PACKAGED') \
        .exclude(status='DELIVERED') \
        .exclude(status='PENDED') \
        .exclude(status='PAID') \
        .exclude(status='REFUNDED') \
        .order_by('created_at')

    confirmed_orders = orders.filter(status='CONFIRMED').order_by('updated_at')
    processed_orders = orders.filter(status='PROCESSED').order_by('updated_at')
    packaged_orders = orders.filter(status='PACKAGED').order_by('updated_at')
    delivered_orders = orders.filter(status='DELIVERED').order_by('updated_at')

    return {
        'new_orders': new_orders,
        'confirmed_orders': confirmed_orders,
        'processed_orders': processed_orders,
        'packaged_orders': packaged_orders,
        'delivered_orders': delivered_orders,
    }




def confirmed(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'CONFIRMED'
            order.save()

def no_answer(request):
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

def packaged(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'PACKAGED'
            order.save()

def delivered(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref', False)

        if Order.objects.all().filter(order_ref=order_ref).exists():
            order = Order.objects.all().get(order_ref=order_ref)
            order.status = 'DELIVERED'
            order.save()

            for order_product in order.product.all():
                inventory_product = Product.objects.all().get(sku=order_product.product_sku)
                inventory_product.quantity = inventory_product.quantity - order_product.quantity
                inventory_product.sell_rate += order_product.quantity
                inventory_product.save()
                if not order_product.size_sku == 'main':
                    size_product = Size.objects.all().get(sku=order_product.size_sku)
                    size_product.quantity = size_product.quantity - order_product.quantity
                    size_product.save()




#    if order_product.quantity > inventory_product.quantity:
#        inventory_product.quantity = inventory_product.quantity - order_product.quantity
#        inventory_product.save()
#    else:
#        unavailable_quantity = True
#        return {'unavailable_quantity': unavailable_quantity,