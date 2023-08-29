def orders(request):
    if request.user.is_authenticated:
        new_orders_count = request.user.new_orders_count()
        refund_requests_count = request.user.refund_requests_count()
    else:
        new_orders_count = None
        refund_requests_count = None

    return {
        'new_orders_count': new_orders_count,
        'refund_requests_count': refund_requests_count
    }