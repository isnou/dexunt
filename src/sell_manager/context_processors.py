from .models import Clip


def shop_manager_content(request):
    try:
        raw_clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No clips")

    points = Clip()
    return {
        'points': points,
    }
