import random
import string
from main_shop.models import Layout
from .models import Product, Feature


def main_banner(request, action):
    url = "shop-manager/e-shop.html"
    try:
        layouts = Layout.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type=action).exists():
        layout = layouts.get(type=action)
    else:
        layout = Layout(type=action)

    if request.method == 'POST':
        en_first_title = request.POST.get('en_first_title', False)
        if not en_first_title:
            en_first_title = layout.en_first_title
        en_second_title = request.POST.get('en_second_title', False)
        if not en_second_title:
            en_second_title = layout.en_second_title
        en_third_title = request.POST.get('en_third_title', False)
        if not en_third_title:
            en_third_title = layout.en_third_title
        en_button = request.POST.get('en_button', False)
        if not en_button:
            en_button = layout.en_button

        fr_first_title = request.POST.get('fr_first_title', False)
        if not fr_first_title:
            fr_first_title = layout.fr_first_title
        fr_second_title = request.POST.get('fr_second_title', False)
        if not fr_second_title:
            fr_second_title = layout.fr_second_title
        fr_third_title = request.POST.get('fr_third_title', False)
        if not fr_third_title:
            fr_third_title = layout.fr_third_title
        fr_button = request.POST.get('fr_button', False)
        if not fr_button:
            fr_button = layout.fr_button

        ar_first_title = request.POST.get('ar_first_title', False)
        if not ar_first_title:
            ar_first_title = layout.ar_first_title
        ar_second_title = request.POST.get('ar_second_title', False)
        if not ar_second_title:
            ar_second_title = layout.ar_second_title
        ar_third_title = request.POST.get('ar_third_title', False)
        if not ar_third_title:
            ar_third_title = layout.ar_third_title
        ar_button = request.POST.get('ar_button', False)
        if not ar_button:
            ar_button = layout.ar_button

        link = request.POST.get('link', False)
        if not link:
            link = layout.link

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


def thumb_banner(request, action):
    url = "shop-manager/e-shop.html"
    try:
        layouts = Layout.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type=action).exists():
        layout = layouts.get(type=action)
    else:
        layout = Layout(type=action)

    if request.method == 'POST':
        en_first_title = request.POST.get('en_first_title', False)
        if not en_first_title:
            en_first_title = layout.en_first_title
        en_second_title = request.POST.get('en_second_title', False)
        if not en_second_title:
            en_second_title = layout.en_second_title
        en_button = request.POST.get('en_button', False)
        if not en_button:
            en_button = layout.en_button

        fr_first_title = request.POST.get('fr_first_title', False)
        if not fr_first_title:
            fr_first_title = layout.fr_first_title
        fr_second_title = request.POST.get('fr_second_title', False)
        if not fr_second_title:
            fr_second_title = layout.fr_second_title
        fr_button = request.POST.get('fr_button', False)
        if not fr_button:
            fr_button = layout.fr_button

        ar_first_title = request.POST.get('ar_first_title', False)
        if not ar_first_title:
            ar_first_title = layout.ar_first_title
        ar_second_title = request.POST.get('ar_second_title', False)
        if not ar_second_title:
            ar_second_title = layout.ar_second_title
        ar_button = request.POST.get('ar_button', False)
        if not ar_button:
            ar_button = layout.ar_button

        link = request.POST.get('link', False)
        if not link:
            link = layout.link

        thumb = request.FILES.get('thumb', False)
        if not thumb:
            thumb = layout.thumb
        layout.en_first_title = en_first_title
        layout.en_second_title = en_second_title
        layout.en_button = en_button

        layout.fr_first_title = fr_first_title
        layout.fr_second_title = fr_second_title
        layout.fr_button = fr_button

        layout.ar_first_title = ar_first_title
        layout.ar_second_title = ar_second_title
        layout.ar_button = ar_button

        layout.link = link

        layout.thumb = thumb

        layout.save()

    return {
        'url': url,
    }


def timer_banner(request, action):
    url = "shop-manager/e-shop.html"
    try:
        layouts = Layout.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type=action).exists():
        layout = layouts.get(type=action)
    else:
        layout = Layout(type=action)

    if request.method == 'POST':
        en_first_title = request.POST.get('en_first_title', False)
        if not en_first_title:
            en_first_title = layout.en_first_title
        en_second_title = request.POST.get('en_second_title', False)
        if not en_second_title:
            en_second_title = layout.en_second_title
        en_third_title = request.POST.get('en_third_title', False)
        if not en_third_title:
            en_third_title = layout.en_third_title
        en_button = request.POST.get('en_button', False)
        if not en_button:
            en_button = layout.en_button

        fr_first_title = request.POST.get('fr_first_title', False)
        if not fr_first_title:
            fr_first_title = layout.fr_first_title
        fr_second_title = request.POST.get('fr_second_title', False)
        if not fr_second_title:
            fr_second_title = layout.fr_second_title
        fr_third_title = request.POST.get('fr_third_title', False)
        if not fr_third_title:
            fr_third_title = layout.fr_third_title
        fr_button = request.POST.get('fr_button', False)
        if not fr_button:
            fr_button = layout.fr_button

        ar_first_title = request.POST.get('ar_first_title', False)
        if not ar_first_title:
            ar_first_title = layout.ar_first_title
        ar_second_title = request.POST.get('ar_second_title', False)
        if not ar_second_title:
            ar_second_title = layout.ar_second_title
        ar_third_title = request.POST.get('ar_third_title', False)
        if not ar_third_title:
            ar_third_title = layout.ar_third_title
        ar_button = request.POST.get('ar_button', False)
        if not ar_button:
            ar_button = layout.ar_button

        year = request.POST.get('year', False)
        if not year:
            year = layout.year
        month = request.POST.get('month', False)
        if not month:
            month = layout.month
        day = request.POST.get('day', False)
        if not day:
            day = layout.day

        link = request.POST.get('link', False)
        if not link:
            link = layout.link

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

        layout.year = year
        layout.month = month
        layout.day = day

        layout.link = link

        layout.thumb = thumb

        layout.save()

    return {
        'url': url,
    }
