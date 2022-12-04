import random
import string
from main_shop.models import Layout
from .models import Product, Feature


def main_banner(request, detail):
    url = "shop-manager/e-shop.html"
    try:
        layouts = Layout.objects.all()
    except Layout.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type=detail).exists():
        layout = layouts.get(type=detail)
    else:
        layout = Layout(type=detail)

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


def thumb_banner(request, detail):
    url = "shop-manager/e-shop.html"
    try:
        layouts = Layout.objects.all()
    except Layout.DoesNotExist:
        raise Http404("No products")

    if layouts.filter(type=detail).exists():
        layout = layouts.get(type=detail)
    else:
        layout = Layout(type=detail)

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


def add_movable_banner(request):
    url = "shop-manager/e-shop.html"
    rank = Layout.objects.all().filter(type='showcase').count() + 1

    if request.method == 'POST':
        en_second_title = request.POST.get('selected_type', False)

        en_first_title = request.POST.get('en_title', False)
        en_third_title = request.POST.get('en_message', False)
        en_button = request.POST.get('en_button', False)

        fr_first_title = request.POST.get('fr_title', False)
        fr_third_title = request.POST.get('fr_message', False)
        fr_button = request.POST.get('fr_button', False)

        ar_first_title = request.POST.get('ar_title', False)
        ar_third_title = request.POST.get('ar_message', False)
        ar_button = request.POST.get('ar_button', False)

        thumb = request.FILES.get('thumb', False)

        link = request.POST.get('link', False)
        layout = Layout(en_second_title=en_second_title,
                        en_first_title=en_first_title,
                        en_third_title=en_third_title,
                        en_button=en_button,
                        fr_first_title=fr_first_title,
                        fr_third_title=fr_third_title,
                        fr_button=fr_button,
                        ar_first_title=ar_first_title,
                        ar_third_title=ar_third_title,
                        ar_button=ar_button,
                        link=link,
                        thumb=thumb,
                        type='showcase',
                        rank=rank,
                        )
        layout.save()

    return {
        'url': url,
    }


def add_showcase(request):
    url = "shop-manager/e-shop.html"
    rank = Layout.objects.all().filter(type='showcase').count() + 1

    if request.method == 'POST':
        en_second_title = request.POST.get('selected_type', False)

        en_first_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)

        fr_first_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)

        ar_first_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)

        link = request.POST.get('link', False)
        layout = Layout(en_second_title=en_second_title,
                        en_first_title=en_first_title,
                        en_button=en_button,
                        fr_first_title=fr_first_title,
                        fr_button=fr_button,
                        ar_first_title=ar_first_title,
                        ar_button=ar_button,
                        link=link,
                        type='showcase',
                        rank=rank,
                        )
        layout.save()

    return {
        'url': url,
    }


def delete(identity):
    url = "shop-manager/e-shop.html"
    ranked_layouts = Layout.objects.all().filter(type='showcase').order_by('rank')
    Layout.objects.all().get(id=identity).delete()
    rank = 1
    for selected_layout in ranked_layouts:
        selected_layout.rank = rank
        rank += 1
        selected_layout.save()

    return {
        'url': url,
    }


def up(identity):
    url = "shop-manager/e-shop.html"
    selected_layouts = Layout.objects.all().filter(type='showcase')
    max_rank = selected_layouts.count()
    initial_selected_layout = selected_layouts.get(id=identity)
    initial_selected_layout_rank = initial_selected_layout.rank
    if initial_selected_layout_rank < max_rank:
        next_selected_layout = selected_layouts.get(rank=initial_selected_layout_rank + 1)
        next_selected_layout_rank = next_selected_layout.rank

        next_selected_layout.rank = initial_selected_layout_rank
        next_selected_layout.save()
        initial_selected_layout.rank = next_selected_layout_rank
        initial_selected_layout.save()

    return {
        'url': url,
    }


def down(identity):
    url = "shop-manager/e-shop.html"
    selected_layouts = Layout.objects.all().filter(type='showcase')
    initial_selected_layout = selected_layouts.get(id=identity)
    initial_selected_layout_rank = initial_selected_layout.rank
    if initial_selected_layout_rank > 1:
        next_selected_layout = selected_layouts.get(rank=initial_selected_layout_rank - 1)
        next_selected_layout_rank = next_selected_layout.rank

        next_selected_layout.rank = initial_selected_layout_rank
        next_selected_layout.save()
        initial_selected_layout.rank = next_selected_layout_rank
        initial_selected_layout.save()

    return {
        'url': url,
    }


def showcase(request, identity):
    url = "shop-manager/e-shop-edit.html"
    selected_layout = Layout.objects.all().get(id=identity)

    if request.method == 'POST':
        en_second_title = request.POST.get('selected_type', False)
        selected_layout.en_second_title = en_second_title

        en_first_title = request.POST.get('en_title', False)
        if en_first_title:
            selected_layout.en_first_title = en_first_title
        en_button = request.POST.get('en_button', False)
        if en_button:
            selected_layout.en_button = en_button

        fr_first_title = request.POST.get('fr_title', False)
        if fr_first_title:
            selected_layout.fr_first_title = fr_first_title
        fr_button = request.POST.get('fr_button', False)
        if fr_button:
            selected_layout.fr_button = fr_button

        ar_first_title = request.POST.get('ar_title', False)
        if ar_first_title:
            selected_layout.ar_first_title = ar_first_title
        ar_button = request.POST.get('ar_button', False)
        if ar_button:
            selected_layout.ar_button = ar_button

        link = request.POST.get('link', False)
        if link:
            selected_layout.link = link
        selected_layout.save()

    return {
        'url': url,
    }
