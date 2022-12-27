from sell_manager.models import Clip
from .models import Product


def points(request):
    url = "/shop-manager/e-shop.html"
    try:
        products = Product.objects.all().exclude(type='photo')
    except Product.DoesNotExist:
        raise Http404("No products")

    try:
        clips = Clip.objects.all()
    except Clips.DoesNotExist:
        raise Http404("No clips")

    if clips.filter(type='points').exists():
        points_clip = clips.get(type='points')
    else:
        points_clip = Clip(type='points')

    if request.method == 'POST':
        en_clip_title = request.POST.get('en_clip_title', False)
        if not en_clip_title:
            en_clip_title = points_clip.en_clip_title

        fr_clip_title = request.POST.get('fr_clip_title', False)
        if not fr_clip_title:
            fr_clip_title = points_clip.fr_clip_title

        ar_clip_title = request.POST.get('ar_clip_title', False)
        if not ar_clip_title:
            ar_clip_title = points_clip.ar_clip_title

        points_clip.en_clip_title = en_clip_title
        points_clip.fr_clip_title = fr_clip_title
        points_clip.ar_clip_title = ar_clip_title

        points_clip.save()

        if clips.filter(type='points-products').exists():
            clips_products = clips.filter(type='points-products')
            for clips_product in clips_products:
                clips_product.en_clip_title = en_clip_title
                clips_product.fr_clip_title = fr_clip_title
                clips_product.ar_clip_title = ar_clip_title
                clips_product.save()

    for product in products:
        if not clips.filter(type='points-products').filter(sku=product.sku).exists():
            new_clip = Clip(type='points-products',
                            sku=product.sku,
                            product_title=product.en_product_title + ' - ' + product.en_variant,
                            thumb=product.thumb,
                            en_clip_title=points_clip.en_clip_title,
                            fr_clip_title=points_clip.fr_clip_title,
                            ar_clip_title=points_clip.ar_clip_title,
                            )
            if product.type == 'size':
                new_clip.product_title = product.en_product_title + ' - ' + product.en_variant + ' - ' + product.size
            if product.type == 'set':
                new_clip.product_title = product.en_product_title + ' - product set - ' + product.en_variant
            new_clip.save()

    return {
        'url': url,
    }


def delivery(request):
    url = "/shop-manager/e-shop.html"
    try:
        products = Product.objects.all().exclude(type='photo').order_by('en_product_title', 'en_variant')
    except Product.DoesNotExist:
        raise Http404("No products")

    try:
        clips = Clip.objects.all()
    except Clips.DoesNotExist:
        raise Http404("No clips")

    if clips.filter(type='delivery').exists():
        points_clip = clips.get(type='delivery')
    else:
        points_clip = Clip(type='delivery')

    if request.method == 'POST':
        en_clip_title = request.POST.get('en_clip_title', False)
        if not en_clip_title:
            en_clip_title = points_clip.en_clip_title

        fr_clip_title = request.POST.get('fr_clip_title', False)
        if not fr_clip_title:
            fr_clip_title = points_clip.fr_clip_title

        ar_clip_title = request.POST.get('ar_clip_title', False)
        if not ar_clip_title:
            ar_clip_title = points_clip.ar_clip_title

        points_clip.en_clip_title = en_clip_title
        points_clip.fr_clip_title = fr_clip_title
        points_clip.ar_clip_title = ar_clip_title

        points_clip.save()

        if clips.filter(type='delivery-products').exists():
            clips_products = clips.filter(type='delivery-products')
            for clips_product in clips_products:
                clips_product.en_clip_title = en_clip_title
                clips_product.fr_clip_title = fr_clip_title
                clips_product.ar_clip_title = ar_clip_title
                clips_product.save()

    for product in products:
        if not clips.filter(type='delivery-products').filter(sku=product.sku).exists():
            new_clip = Clip(type='delivery-products',
                            sku=product.sku,
                            product_title=product.en_product_title + ' - ' + product.en_variant,
                            thumb=product.thumb,

                            en_clip_title=points_clip.en_clip_title,
                            fr_clip_title=points_clip.fr_clip_title,
                            ar_clip_title=points_clip.ar_clip_title,
                            )
            new_clip.save()

    return {
        'url': url,
    }


def solidarity(request):
    url = "/shop-manager/e-shop.html"
    try:
        products = Product.objects.all().exclude(type='photo').order_by('en_product_title', 'en_variant')
    except Product.DoesNotExist:
        raise Http404("No products")

    try:
        clips = Clip.objects.all()
    except Clips.DoesNotExist:
        raise Http404("No clips")

    if clips.filter(type='solidarity').exists():
        points_clip = clips.get(type='solidarity')
    else:
        points_clip = Clip(type='solidarity')

    if request.method == 'POST':
        en_clip_title = request.POST.get('en_clip_title', False)
        if not en_clip_title:
            en_clip_title = points_clip.en_clip_title

        fr_clip_title = request.POST.get('fr_clip_title', False)
        if not fr_clip_title:
            fr_clip_title = points_clip.fr_clip_title

        ar_clip_title = request.POST.get('ar_clip_title', False)
        if not ar_clip_title:
            ar_clip_title = points_clip.ar_clip_title

        points_clip.en_clip_title = en_clip_title
        points_clip.fr_clip_title = fr_clip_title
        points_clip.ar_clip_title = ar_clip_title

        points_clip.save()

        if clips.filter(type='solidarity-products').exists():
            clips_products = clips.filter(type='solidarity-products')
            for clips_product in clips_products:
                clips_product.en_clip_title = en_clip_title
                clips_product.fr_clip_title = fr_clip_title
                clips_product.ar_clip_title = ar_clip_title
                clips_product.save()

    for product in products:
        if not clips.filter(type='solidarity-products').filter(sku=product.sku).exists():
            new_clip = Clip(type='solidarity-products',
                            sku=product.sku,
                            product_title=product.en_product_title + ' - ' + product.en_variant,
                            thumb=product.thumb,

                            en_clip_title=points_clip.en_clip_title,
                            fr_clip_title=points_clip.fr_clip_title,
                            ar_clip_title=points_clip.ar_clip_title,
                            )
            new_clip.save()

    return {
        'url': url,
    }


def points_to_product(request, index):
    url = "/shop-manager/e-shop.html"
    clip = Clip.objects.all().get(id=index)
    if request.method == 'POST':
        clip.points = int(request.POST.get('points_value', False))
        clip.save()

    return {
        'url': url,
    }


def value_to_product(request, index):
    url = "/shop-manager/e-shop.html"
    clip = Clip.objects.all().get(id=index)
    if request.method == 'POST':
        clip.value = int(request.POST.get('clip_value', False))
        clip.save()

    return {
        'url': url,
    }
