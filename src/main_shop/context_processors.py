from .models import Intro, Showcase, Category, RootDirectory, SubDirectory


def main_shop_content(request):
    intro = Intro.objects.all().get(id=1)

    try:
        showcases = Showcase.objects.all().order_by('-rank')
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    try:
        root_directories = RootDirectory.objects.all().order_by('-rank')
    except RootDirectory.objects.all().DoesNotExist:
        raise Http404("No directories")

    return {
        'intro': intro,
        'showcases': showcases,
        'root_directories': root_directories,
    }
