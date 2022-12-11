from .models import Clip


def shop_manager_content(request):
    try:
        raw_clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No products")

    if raw_clips.filter(type='points').exists():
        points = raw_clips.get(type='points')
    else:
        points = None
    return {
        'points': points,
    }
