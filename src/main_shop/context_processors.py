from .models import Intro, Showcase, Category


def main_shop_content(request):
    intro = Intro.objects.all().get(id=1)

    try:
        showcases = Showcase.objects.all().order_by('-rank')
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")
    try:
        categories = Category.objects.all().order_by('-rank')
    except Category.objects.all().DoesNotExist:
        raise Http404("No categories")

    return {
        'intro': intro,
        'showcases': showcases,
        'categories': categories,
    }
