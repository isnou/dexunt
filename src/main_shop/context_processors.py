from .models import IntroBanner, IntroThumb, Showcase


def main_shop_content(request):
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

    return {
        'intro_thumbs': intro_thumbs,
        'intro_banners': intro_banners,
        'showcases': showcases,
    }
