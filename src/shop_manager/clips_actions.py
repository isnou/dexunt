from sell_manager.models import Clip
from .models import Product


def add_points(request):
    url = "/shop-manager/e-shop.html"

    if request.method == 'POST':
        en_second_title = request.POST.get('selected_type', False)

        en_first_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)

        fr_first_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)

        ar_first_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)

        link = request.POST.get('link', False)
        layout = Layout(en_second_title=en_second_title,
                        en_first_title=en_first_title,
                        en_button=en_button,
                        fr_first_title=fr_first_title,
                        fr_button=fr_button,
                        ar_first_title=ar_first_title,
                        ar_button=ar_button,
                        link=link,
                        type='showcase',
                        rank=rank,
                        )
        layout.save()

    return {
        'url': url,
    }
