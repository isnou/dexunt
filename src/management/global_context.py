def orders(request):
    if request.user.is_authenticated:
        new_orders_count = request.user.new_orders_count()
        refund_requests = request.user.refund_requests()
    else:
        new_orders_count = None
        refund_requests = None

    return {
        'new_orders_count': new_orders_count,
        'refund_requests': refund_requests
    }