from .models import Clip
# from shop_manager.models import Product


def clips_manager(request):
    try:
        raw_clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No clips")

    if raw_clips.filter(type='points').exists():
        points = raw_clips.get(type='points')
    else:
        points = Clip()

    if raw_clips.filter(type='points-products').exists():
        points_products = Clip()
    else:
        points_products = Clip()

    return {
        'points': points,
        'points_products': points_products,
    }
