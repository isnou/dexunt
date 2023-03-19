from .models import Intro, Showcase, Category, Directory, Department


def main_shop_content(request):
    if not Intro.objects.all().filter(id=1).exists():
        intro = Intro(id=1, )
        intro.save()
    else:
        intro = Intro.objects.all().get(id=1)

    try:
        showcases = Showcase.objects.all().order_by('-rank')
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    try:
        departments = Department.objects.all()
    except Department.objects.all().DoesNotExist:
        raise Http404("No directories")

    return {
        'intro': intro,
        'showcases': showcases,
        'departments': departments,
    }
