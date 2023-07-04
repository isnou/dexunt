from main_home.models import Order

def orders(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            new_orders_count = Order.objects.all().filter(status='FULFILLED').count()
        else:
            new_orders_count = None
    else:
        new_orders_count = None

    return {
        'new_orders_count': new_orders_count
    }