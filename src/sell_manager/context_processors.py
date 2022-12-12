from .models import Clip
# from shop_manager.models import Product


def clips_manager(request):
    try:
        raw_clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No clips")

    try:
        products = Product.objects.all().filter(type='main')
    except Product.DoesNotExist:
        raise Http404("No products")

    if raw_clips.filter(type='points').exists():
        points = raw_clips.get(type='points')
    else:
        points = Clip()

    if raw_clips.filter(type='points-products').exists():
        points_products = raw_clips.get(type='points-products')
    else:
        points_products = Clip()

    return {
        'points': points,
        'points_products': points_products,
    }
