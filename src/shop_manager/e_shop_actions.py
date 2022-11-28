import random
import string
from main_shop.models import Layout
from .models import Product, Feature


def edit_first_main_banner(request):
    url = "shop-manager/e-shop.html"
    try:
        layouts = Layout.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type='first_main_banner').exists():
        layout = layouts.get(type='first_main_banner')
    else:
        layout = Layout(type='first_main_banner')

    if request.method == 'POST':
        en_first_title = request.POST.get('en_first_title', False)
        en_second_title = request.POST.get('en_second_title', False)
        en_third_title = request.POST.get('en_third_title', False)
        en_button = request.POST.get('en_button', False)

        fr_first_title = request.POST.get('fr_first_title', False)
        fr_second_title = request.POST.get('fr_second_title', False)
        fr_third_title = request.POST.get('fr_third_title', False)
        fr_button = request.POST.get('fr_button', False)

        ar_first_title = request.POST.get('ar_first_title', False)
        ar_second_title = request.POST.get('ar_second_title', False)
        ar_third_title = request.POST.get('ar_third_title', False)
        ar_button = request.POST.get('ar_button', False)

        link = request.POST.get('link', False)

        thumb = request.FILES.get('thumb', False)
        if not thumb:
            thumb = layout.thumb
        layout.en_first_title = en_first_title
        layout.en_second_title = en_second_title
        layout.en_third_title = en_third_title
        layout.en_button = en_button

        layout.fr_first_title = fr_first_title
        layout.fr_second_title = fr_second_title
        layout.fr_third_title = fr_third_title
        layout.fr_button = fr_button

        layout.ar_first_title = ar_first_title
        layout.ar_second_title = ar_second_title
        layout.ar_third_title = ar_third_title
        layout.ar_button = ar_button

        layout.link = link

        layout.thumb = thumb

        layout.save()

    return {
        'url': url,
    }
