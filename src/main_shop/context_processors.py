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

    if layouts.filter(type='first_main_banner').exists():
        first_main_banner = layouts.get(type='first_main_banner')
    else:
        first_main_banner = Layout()
    return {
        'expiration_date': expiration_date,
        'first_main_banner': first_main_banner,
    }
