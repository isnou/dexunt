from .models import Content


def extras(request):
    content = Content.objects.all()
    en = content.all().filter(lang='EN')
    fr = content.all().filter(lang='FR')
    ar = content.all().filter(lang='AR')
    return {
        'en': en,
        'fr': fr,
        'ar': ar,
    }
