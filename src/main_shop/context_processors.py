from .models import Intro, IntroBanner, IntroThumb, Showcase, Category


def main_shop_content(request):
    intro = Intro.objects.all().get(id=1)

    try:
        intro_thumbs = IntroThumb.objects.all().order_by('rank')
    except IntroThumb.objects.all().DoesNotExist:
        raise Http404("No thumbs")
    try:
        intro_banners = IntroBanner.objects.all().order_by('rank')
    except IntroBanner.objects.all().DoesNotExist:
        raise Http404("No banners")
    try:
        showcases = Showcase.objects.all().order_by('-rank')
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")
    try:
        categories = Category.objects.all().order_by('-rank')
    except Category.objects.all().DoesNotExist:
        raise Http404("No categories")

    return {
        'intro_thumbs': intro_thumbs,
        'intro_banners': intro_banners,
        'showcases': showcases,
        'categories': categories,
        'intro': intro,
    }
