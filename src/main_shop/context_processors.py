from .models import Content


def extras(request):
    content = Content.objects.all()
    en = content.filter(lang='EN')
    fr = content.filter(lang='FR')
    ar = content.filter(lang='AR')
    return {
        'en': en,
        'fr': fr,
        'ar': ar,
    }
