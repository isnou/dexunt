from .models import Clip


def shop_manager_content(request):
    try:
        raw_clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No clips")

    if raw_clips.filter(type='poi').exists():
        points = raw_clips.get(type='poi')
    else:
        points = Clip()
    return {
        'points': points,
    }
