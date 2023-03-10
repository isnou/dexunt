import random
import string
from main_shop.models import IntroThumb, IntroBanner ,Showcase
from .models import Product, Feature

def initialisation():
    try:
        intro_banners = IntroBanner.objects.all()
    except IntroBanner.DoesNotExist:
        raise Http404("No banners")
    try:
        intro_thumbs = IntroThumb.objects.all()
    except IntroThumb.DoesNotExist:
        raise Http404("No thumbs")

    if not intro_banners.filter(rank=1).exists():
        IntroBanner(en_title='first',
                    rank=1,
                    ).save()
    if not intro_banners.filter(rank=2).exists():
        IntroBanner(en_title='second',
                    rank=2,
                    ).save()
    if not intro_banners.filter(rank=3).exists():
        IntroBanner(en_title='third',
                    rank=3,
                    ).save()

    if not intro_thumbs.filter(rank=1).exists():
        IntroThumb(en_title='first',
                    rank=1,
                    ).save()
    if not intro_thumbs.filter(rank=2).exists():
        IntroThumb(en_title='second',
                    rank=2,
                    ).save()
    if not intro_thumbs.filter(rank=3).exists():
        IntroThumb(en_title='third',
                    rank=3,
                    ).save()

    return {
        'intro_banners': intro_banners,
        'intro_thumbs':intro_thumbs,
    }

# -----------------------------intro banner
def edit_banner(request, index):
    url = "/shop-manager/e-shop.html"
    try:
        intro_banner = IntroBanner.objects.all().get(rank=index)
    except IntroBanner.objects.all().DoesNotExist:
        raise Http404("No banners")

    if request.method == 'POST':

        en_intro = request.POST.get('en_intro', False)
        en_title = request.POST.get('en_title', False)
        en_description = request.POST.get('en_description', False)
        en_button = request.POST.get('en_button', False)
        fr_intro = request.POST.get('fr_intro', False)
        fr_title = request.POST.get('fr_title', False)
        fr_description = request.POST.get('fr_description', False)
        fr_button = request.POST.get('fr_button', False)
        ar_intro = request.POST.get('ar_intro', False)
        ar_title = request.POST.get('ar_title', False)
        ar_description = request.POST.get('ar_description', False)
        ar_button = request.POST.get('ar_button', False)
        button_link = request.POST.get('button_link', False)
        thumb = request.FILES.get('thumb', False)

        if en_intro:
            intro_banner.en_intro = en_intro
        if en_title:
            intro_banner.en_title = en_title
        if en_description:
            intro_banner.en_description = en_description
        if en_button:
            intro_banner.en_button = en_button

        if fr_intro:
            intro_banner.fr_intro = fr_intro
        if fr_title:
            intro_banner.fr_title = fr_title
        if fr_description:
            intro_banner.fr_description = fr_description
        if fr_button:
            intro_banner.fr_button = fr_button

        if ar_intro:
            intro_banner.ar_intro = ar_intro
        if ar_title:
            intro_banner.ar_title = ar_title
        if ar_description:
            intro_banner.ar_description = ar_description
        if ar_button:
            intro_banner.ar_button = ar_button

        if button_link:
            intro_banner.link = button_link

        if thumb:
            intro_banner.thumb = thumb

        intro_banner.save()

    return {
        'url': url,
    }

def up_banner(index):
    url = "/shop-manager/e-shop.html"
    selected_intro_banner = IntroBanner.objects.all().get(rank=index)

    if not index == 3:
        next_intro_banner = IntroBanner.objects.all().get(rank=index+1)
    else:
        next_intro_banner = IntroBanner.objects.all().get(rank=1)
    rank = selected_intro_banner.rank
    next_rank = next_intro_banner.rank

    selected_intro_banner.rank = next_rank
    next_intro_banner.rank = rank

    selected_intro_banner.save()
    next_intro_banner.save()

    return {
        'url': url,
    }

def down_banner(index):
    url = "/shop-manager/e-shop.html"
    selected_intro_banner = IntroBanner.objects.all().get(rank=index)

    if not index == 1:
        next_intro_banner = IntroBanner.objects.all().get(rank=index-1)
    else:
        next_intro_banner = IntroBanner.objects.all().get(rank=3)
    rank = selected_intro_banner.rank
    next_rank = next_intro_banner.rank

    selected_intro_banner.rank = next_rank
    next_intro_banner.rank = rank

    selected_intro_banner.save()
    next_intro_banner.save()

    return {
        'url': url,
    }

# -----------------------------intro thumb
def edit_thumb(request, index):
    url = "/shop-manager/e-shop.html"
    try:
        intro_thumb = IntroThumb.objects.all().get(rank=index)
    except IntroThumb.objects.all().DoesNotExist:
        raise Http404("No banners")

    if request.method == 'POST':

        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        button_link = request.POST.get('button_link', False)
        thumb = request.FILES.get('thumb', False)

        if en_title:
            intro_thumb.en_title = en_title
        if en_button:
            intro_thumb.en_button = en_button

        if fr_title:
            intro_thumb.fr_title = fr_title
        if fr_button:
            intro_thumb.fr_button = fr_button

        if ar_title:
            intro_thumb.ar_title = ar_title
        if ar_button:
            intro_thumb.ar_button = ar_button

        if button_link:
            intro_thumb.link = button_link

        if thumb:
            intro_thumb.thumb = thumb

        intro_thumb.save()

    return {
        'url': url,
    }

def up_thumb(index):
    url = "/shop-manager/e-shop.html"
    selected_intro_thumb = IntroThumb.objects.all().get(rank=index)

    if not index == 3:
        next_intro_thumb = IntroThumb.objects.all().get(rank=index+1)
    else:
        next_intro_thumb = IntroThumb.objects.all().get(rank=1)
    rank = selected_intro_thumb.rank
    next_rank = next_intro_thumb.rank

    selected_intro_thumb.rank = next_rank
    next_intro_thumb.rank = rank

    selected_intro_thumb.save()
    next_intro_thumb.save()

    return {
        'url': url,
    }

def down_thumb(index):
    url = "/shop-manager/e-shop.html"
    selected_intro_thumb = IntroThumb.objects.all().get(rank=index)

    if not index == 1:
        next_intro_thumb = IntroThumb.objects.all().get(rank=index-1)
    else:
        next_intro_thumb = IntroThumb.objects.all().get(rank=3)
    rank = selected_intro_thumb.rank
    next_rank = next_intro_thumb.rank

    selected_intro_thumb.rank = next_rank
    next_intro_thumb.rank = rank

    selected_intro_thumb.save()
    next_intro_thumb.save()

    return {
        'url': url,
    }

# -----------------------------ad & showcase
def edit_single_flash(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='single_flash'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        url = request.POST.get('link', False)
        thumb = request.FILES.get('thumb', False)
        day = request.POST.get('day', False)
        month = request.POST.get('month', False)
        year = request.POST.get('year', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if url:
            selected_showcase.link = url

        if thumb:
            selected_showcase.thumb = thumb

        if day:
            selected_showcase.day = day
        if month:
            selected_showcase.month = month
        if year:
            selected_showcase.year = year

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_multiple_flash(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='multiple_flash'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        day = request.POST.get('day', False)
        month = request.POST.get('month', False)
        year = request.POST.get('year', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if day:
            selected_showcase.day = day
        if month:
            selected_showcase.month = month
        if year:
            selected_showcase.year = year

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_grid_showcase(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='grid_showcase'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_slider_showcase(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='slider_showcase'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_small_ad(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='small_ad'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        url = request.POST.get('link', False)
        thumb = request.FILES.get('thumb', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if url:
            selected_showcase.link = url

        if thumb:
            selected_showcase.thumb = thumb

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_big_ad(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='big_ad'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        url = request.POST.get('link', False)
        thumb = request.FILES.get('thumb', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if url:
            selected_showcase.link = url

        if thumb:
            selected_showcase.thumb = thumb

        selected_showcase.save()

    return {
        'url': url,
    }

def up_showcase(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_showcase = Showcase.objects.all().get(sku=detail)
    max_rank = Showcase.objects.all().count()

    if index == max_rank:
        next_showcase = Showcase.objects.all().get(rank=1)
    else:
        next_showcase = Showcase.objects.all().get(rank=index + 1)

    selected_showcase.rank = next_showcase.rank
    next_showcase.rank = index

    selected_showcase.save()
    next_showcase.save()

    return {
        'url': url,
    }

def down_showcase(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_showcase = Showcase.objects.all().get(sku=detail)
    max_rank = Showcase.objects.all().count()

    if index == 1:
        next_showcase = Showcase.objects.all().get(rank=max_rank)
    else:
        next_showcase = Showcase.objects.all().get(rank=index - 1)

    selected_showcase.rank = next_showcase.rank
    next_showcase.rank = index

    selected_showcase.save()
    next_showcase.save()

    return {
        'url': url,
    }





def add_movable_banner(request):
    url = "/shop-manager/e-shop.html"
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

        year = request.POST.get('year', False)
        month = request.POST.get('month', False)
        day = request.POST.get('day', False)

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
                        year=year,
                        day=day,
                        month=month,
                        thumb=thumb,
                        link=link,
                        type='showcase',
                        rank=rank,
                        )
        layout.save()

    return {
        'url': url,
    }


def add_showcase(request):
    url = "/shop-manager/e-shop.html"
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



def up(index):
    url = "/shop-manager/e-shop.html"
    selected_layouts = Layout.objects.all().filter(type='showcase')
    max_rank = selected_layouts.count()
    initial_selected_layout = selected_layouts.get(id=index)
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


def down(index):
    url = "/shop-manager/e-shop.html"
    selected_layouts = Layout.objects.all().filter(type='showcase')
    initial_selected_layout = selected_layouts.get(id=index)
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


def showcase(request, index):
    url = "/shop-manager/e-shop.html"
    selected_layout = Layout.objects.all().get(id=index)

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


def banner(request, index):
    url = "/shop-manager/e-shop.html"
    selected_layout = Layout.objects.all().get(id=index)

    if request.method == 'POST':
        en_second_title = request.POST.get('selected_type', False)
        selected_layout.en_second_title = en_second_title

        en_first_title = request.POST.get('en_title', False)
        if en_first_title:
            selected_layout.en_first_title = en_first_title
        en_third_title = request.POST.get('en_message', False)
        if en_third_title:
            selected_layout.en_third_title = en_third_title
        en_button = request.POST.get('en_button', False)
        if en_button:
            selected_layout.en_button = en_button

        fr_first_title = request.POST.get('fr_title', False)
        if fr_first_title:
            selected_layout.fr_first_title = fr_first_title
        fr_third_title = request.POST.get('fr_message', False)
        if fr_third_title:
            selected_layout.fr_third_title = fr_third_title
        fr_button = request.POST.get('fr_button', False)
        if fr_button:
            selected_layout.fr_button = fr_button

        ar_first_title = request.POST.get('ar_title', False)
        if ar_first_title:
            selected_layout.ar_first_title = ar_first_title
        ar_third_title = request.POST.get('ar_message', False)
        if ar_third_title:
            selected_layout.ar_third_title = ar_third_title
        ar_button = request.POST.get('ar_button', False)
        if ar_button:
            selected_layout.ar_button = ar_button

        year = request.POST.get('year', False)
        if year:
            selected_layout.year = year
        month = request.POST.get('month', False)
        if month:
            selected_layout.month = month
        day = request.POST.get('day', False)
        if day:
            selected_layout.day = day

        thumb = request.FILES.get('thumb', False)
        if thumb:
            selected_layout.thumb = thumb

        link = request.POST.get('link', False)
        if link:
            selected_layout.link = link

        selected_layout.save()

    return {
        'url': url,
    }


def link(detail, index):
    url = "/shop-manager/e-shop-edit.html"
    selected_layout = Layout.objects.all().get(id=index)
    selected_product = Product.objects.all().get(sku=detail)
    selected_layout.products.add(selected_product)
    selected_layout.save()

    return {
        'url': url,
    }


def unlink(detail, index):
    url = "/shop-manager/e-shop-edit.html"
    selected_layout = Layout.objects.all().get(id=index)
    selected_product = Product.objects.all().get(sku=detail)
    selected_layout.products.remove(selected_product)
    selected_layout.save()

    return {
        'url': url,
    }

# ------------------ functions
def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str