from .models import Layout


def main_shop_content(request):
    try:
        layouts = Layout.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type='timer_banner').exists():
        expiration_date = layouts.get(type='timer_banner')
    else:
        expiration_date = Layout()
    return {
        'expiration_date': expiration_date,
    }
