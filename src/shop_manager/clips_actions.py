from sell_manager.models import Clip
from .models import Product


def points(request):
    url = "/shop-manager/e-shop.html"
    try:
        products = Product.objects.all()
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
        en_clip_detail = request.POST.get('en_clip_detail', False)
        if not en_clip_detail:
            en_clip_detail = points_clip.en_clip_detail

        fr_clip_title = request.POST.get('fr_clip_title', False)
        if not fr_clip_title:
            fr_clip_title = points_clip.fr_clip_title
        fr_clip_detail = request.POST.get('fr_clip_detail', False)
        if not fr_clip_detail:
            fr_clip_detail = points_clip.fr_clip_detail

        ar_clip_title = request.POST.get('ar_clip_title', False)
        if not ar_clip_title:
            ar_clip_title = points_clip.ar_clip_title
        ar_clip_detail = request.POST.get('ar_clip_detail', False)
        if not ar_clip_detail:
            ar_clip_detail = points_clip.ar_clip_detail

        points_clip.en_clip_title = en_clip_title
        points_clip.en_clip_detail = en_clip_detail

        points_clip.fr_clip_title = fr_clip_title
        points_clip.fr_clip_detail = fr_clip_detail

        points_clip.ar_clip_title = ar_clip_title
        points_clip.ar_clip_detail = ar_clip_detail

        points_clip.save()

    for product in products:
        if not clips.filter(type='points-products').filter(sku=product.sku).exists():
            new_clip = Clip(type='points-products',
                            sku=product.sku,
                            product_title=product.en_product_title + ' - ' + product.en_variant,
                            thumb=product.thumb,

                            en_clip_title=points_clip.en_clip_title,
                            en_clip_detail=points_clip.en_clip_detail,

                            fr_clip_title=points_clip.fr_clip_title,
                            fr_clip_detail=points_clip.fr_clip_detail,

                            ar_clip_title=points_clip.ar_clip_title,
                            ar_clip_detail=points_clip.ar_clip_detail,
                            )
            new_clip.save()

    return {
        'url': url,
    }


def points_to_product(detail):
    url = "/shop-manager/e-shop.html"
    try:
        clips = Clip.objects.all()
    except Clips.DoesNotExist:
        raise Http404("No clips")
    clip_info = clips.get(type='points')

    try:
        products = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No products")
    product_info = products.get(sku=detail)

    if not clips.filter(type='points-products').filter(sku=detail).exists():
        new_clip = Clip(type='points-products',
                        sku=detail,
                        product_title=product_info.en_product_title + ' - ' + product_info.en_variant,
                        thumb=product_info.thumb,

                        en_clip_title=clip_info.en_clip_title,
                        en_clip_detail=clip_info.en_clip_detail,

                        fr_clip_title=clip_info.fr_clip_title,
                        fr_clip_detail=clip_info.fr_clip_detail,

                        ar_clip_title=clip_info.ar_clip_title,
                        ar_clip_detail=clip_info.ar_clip_detail,
                        )
        new_clip.save()

    return {
        'url': url,
    }