def orders(request):
    if request.user.is_authenticated:
        new_orders_count = request.user.new_orders()
    else:
        new_orders_count = None

    return {
        'new_orders_count': new_orders_count
    }