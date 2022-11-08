from .models import Content


def extras(request):
    content = Content.objects.all()
    en = content.get(lang='EN')
    fr = content.get(lang='FR')
    ar = content.get(lang='AR')
    return {
        'en': en,
        'fr': fr,
        'ar': ar,
    }
