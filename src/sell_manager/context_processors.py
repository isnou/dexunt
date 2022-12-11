from .models import Clip
from shop_manager.models import Product


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

    points_added_products = Product.objects.all().exclude()
    points_products_to_add = products

    if raw_clips.filter(type='points-products').exists():
        all_points = raw_clips.filter(type='points-products')
        for points in all_points:
            points_added_products.add(products.get(sku=points.sku))
            points_products_to_add = products.exclude(sku=points.sku)

    return {
        'points': points,
        'points_added_products': points_added_products,
        'points_products_to_add': points_products_to_add,
    }
