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

    points_added_products = products
    points_products_to_add = products
    for product in products:
        points_added_products.exclude(sku=product.sku)

    return {
        'points': points,
        'points_added_products': points_added_products,
        'points_products_to_add': points_products_to_add,
    }
