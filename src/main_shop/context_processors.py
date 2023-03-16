from .models import Intro, Showcase, Category, Directory


def main_shop_content():
    intro = Intro.objects.all().get(id=1)

    try:
        showcases = Showcase.objects.all().order_by('-rank')
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    try:
        directories = Directory.objects.all().order_by('-rank')
    except Directory.objects.all().DoesNotExist:
        raise Http404("No directories")

    return {
        'intro': intro,
        'showcases': showcases,
        'directories': directories,
    }
