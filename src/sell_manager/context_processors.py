from .models import Clip


def shop_manager_content(request):
    try:
        raw_clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No products")

    points = raw_clips.filter(type='points').order_by('-product_title')
    point_count = points.count()
    return {
        'points': points,
        'point_count': point_count,
    }
