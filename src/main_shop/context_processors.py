from .models import Layout


def main_shop_content(request):
    try:
        layouts = Layout.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    if layouts.filter(type='timer_banner').exists():
        timer_banner = layouts.get(type='timer_banner')
    else:
        timer_banner = Layout()

    if layouts.filter(type='first_main_banner').exists():
        first_main_banner = layouts.get(type='first_main_banner')
    else:
        first_main_banner = Layout()
    if layouts.filter(type='second_main_banner').exists():
        second_main_banner = layouts.get(type='second_main_banner')
    else:
        second_main_banner = Layout()
    if layouts.filter(type='third_main_banner').exists():
        third_main_banner = layouts.get(type='third_main_banner')
    else:
        third_main_banner = Layout()

    if layouts.filter(type='first_thumb_banner').exists():
        first_thumb_banner = layouts.get(type='first_thumb_banner')
    else:
        first_thumb_banner = Layout()
    if layouts.filter(type='second_thumb_banner').exists():
        second_thumb_banner = layouts.get(type='second_thumb_banner')
    else:
        second_thumb_banner = Layout()
    if layouts.filter(type='third_thumb_banner').exists():
        third_thumb_banner = layouts.get(type='third_thumb_banner')
    else:
        third_thumb_banner = Layout()

    if layouts.filter(type='showcase').exists():
        showcases = layouts.filter(type='showcase').order_by('rank')
    else:
        showcases = Layout()
    return {
        'timer_banner': timer_banner,

        'first_main_banner': first_main_banner,
        'second_main_banner': second_main_banner,
        'third_main_banner': third_main_banner,

        'first_thumb_banner': first_thumb_banner,
        'second_thumb_banner': second_thumb_banner,
        'third_thumb_banner': third_thumb_banner,

        'showcases': showcases,
    }
