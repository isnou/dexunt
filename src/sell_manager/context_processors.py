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

    if raw_clips.filter(type='delivery').exists():
        delivery = raw_clips.get(type='delivery')
    else:
        delivery = Clip()

    if raw_clips.filter(type='solidarity').exists():
        solidarity = raw_clips.get(type='solidarity')
    else:
        solidarity = Clip()

    if raw_clips.filter(type='points-products').exists():
        points_products = raw_clips.filter(type='points-products')
    else:
        points_products = None

    if raw_clips.filter(type='delivery-products').exists():
        delivery_products = raw_clips.filter(type='delivery-products')
    else:
        delivery_products = None

    if raw_clips.filter(type='solidarity-products').exists():
        solidarity_products = raw_clips.filter(type='solidarity-products')
    else:
        solidarity_products = None

    return {
        'points': points,
        'delivery': delivery,
        'solidarity': solidarity,
        'points_products': points_products,
        'delivery_products': delivery_products,
        'solidarity_products': solidarity_products,
    }
