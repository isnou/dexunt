from .models import Content


def main_page_content(request):
    return {
        'en': en,
        'fr': fr,
        'ar': ar,
    }
