from .models import IntroBanner, IntroThumb, Showcase


def main_shop_content(request):
    try:
        intro_thumbs = IntroThumb.objects.all()
    except IntroThumb.objects.all().DoesNotExist:
        raise Http404("No thumbs")
    try:
        intro_banners = IntroBanner.objects.all()
    except IntroBanner.objects.all().DoesNotExist:
        raise Http404("No banners")

    return {
        'intro_thumbs': intro_thumbs,
        'intro_banners': intro_banners,

        'showcases_exists': None,
        'showcases': None,
    }
