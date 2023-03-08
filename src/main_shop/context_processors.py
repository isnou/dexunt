from .models import IntroBanner, IntroThumb, Showcase


def main_shop_content(request):

    return {
        'first_main_banner': None,
        'second_main_banner': None,
        'third_main_banner': None,

        'first_thumb_banner': None,
        'second_thumb_banner': None,
        'third_thumb_banner': None,

        'showcases_exists': None,
        'showcases': None,
    }
