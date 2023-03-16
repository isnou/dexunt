import random
import string
from main_shop.models import Intro ,Showcase ,Directory ,Category
from .models import Product, Feature

# -----------------------------intro
def edit_intro(request):
    url = "/shop-manager/e-shop.html"

    if request.method == 'POST':

        color = request.POST.get('color', False)
        banner = request.FILES.get('banner', False)
        margin = request.POST.get('margin', False)

        intro = Intro.objects.all().get(id=1)

        if color:
            intro.color = color
        if banner:
            intro.banner = banner
        if margin:
            intro.margin = int(margin)

        intro.save()

    return {
        'url': url,
    }

# -----------------------------ad & showcase
def edit_single_flash(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='single_flash'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        showcase_url = request.POST.get('showcase_url', False)
        thumb = request.FILES.get('thumb', False)
        day = request.POST.get('day', False)
        month = request.POST.get('month', False)
        year = request.POST.get('year', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if showcase_url:
            selected_showcase.link = showcase_url

        if thumb:
            selected_showcase.thumb = thumb

        if day:
            selected_showcase.day = day
        if month:
            selected_showcase.month = month
        if year:
            selected_showcase.year = year

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_multiple_flash(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='multiple_flash'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        thumb = request.FILES.get('thumb', False)
        day = request.POST.get('day', False)
        month = request.POST.get('month', False)
        year = request.POST.get('year', False)


        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if thumb:
            selected_showcase.thumb = thumb

        if day:
            selected_showcase.day = day
        if month:
            selected_showcase.month = month
        if year:
            selected_showcase.year = year

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_grid_showcase(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='grid_showcase'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_slider_showcase(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='slider_showcase'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)

        if en_title:
            selected_showcase.en_title = en_title

        if fr_title:
            selected_showcase.fr_title = fr_title

        if ar_title:
            selected_showcase.ar_title = ar_title

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_small_ad(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='small_ad'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        showcase_url = request.POST.get('showcase_url', False)
        thumb = request.FILES.get('thumb', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if showcase_url:
            selected_showcase.link = showcase_url

        if thumb:
            selected_showcase.thumb = thumb

        selected_showcase.save()

    return {
        'url': url,
    }

def edit_big_ad(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        showcases = Showcase.objects.all()
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    if not detail =='new':
        try:
            selected_showcase = Showcase.objects.all().get(sku=detail)
        except Showcase.objects.all().DoesNotExist:
            raise Http404("No showcase")
    else:
        selected_showcase = None

    type='big_ad'
    if not selected_showcase:
        sku = serial_number_generator(10).upper()
        if showcases:
            rank = showcases.count() + 1
        else:
            rank = 1
        selected_showcase = Showcase(rank=rank,
                                     type=type,
                                     sku=sku,
                                     )
        selected_showcase.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_button = request.POST.get('en_button', False)
        fr_title = request.POST.get('fr_title', False)
        fr_button = request.POST.get('fr_button', False)
        ar_title = request.POST.get('ar_title', False)
        ar_button = request.POST.get('ar_button', False)
        showcase_url = request.POST.get('showcase_url', False)
        thumb = request.FILES.get('thumb', False)

        if en_title:
            selected_showcase.en_title = en_title
        if en_button:
            selected_showcase.en_button = en_button

        if fr_title:
            selected_showcase.fr_title = fr_title
        if fr_button:
            selected_showcase.fr_button = fr_button

        if ar_title:
            selected_showcase.ar_title = ar_title
        if ar_button:
            selected_showcase.ar_button = ar_button

        if showcase_url:
            selected_showcase.link = showcase_url

        if thumb:
            selected_showcase.thumb = thumb

        selected_showcase.save()

    return {
        'url': url,
    }

def up_showcase(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_showcase = Showcase.objects.all().get(sku=detail)
    max_rank = Showcase.objects.all().count()

    if index == max_rank:
        next_showcase = Showcase.objects.all().get(rank=1)
    else:
        next_showcase = Showcase.objects.all().get(rank=index + 1)

    selected_showcase.rank = next_showcase.rank
    next_showcase.rank = index

    selected_showcase.save()
    next_showcase.save()

    return {
        'url': url,
    }

def down_showcase(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_showcase = Showcase.objects.all().get(sku=detail)
    max_rank = Showcase.objects.all().count()

    if index == 1:
        next_showcase = Showcase.objects.all().get(rank=max_rank)
    else:
        next_showcase = Showcase.objects.all().get(rank=index - 1)

    selected_showcase.rank = next_showcase.rank
    next_showcase.rank = index

    selected_showcase.save()
    next_showcase.save()

    return {
        'url': url,
    }

def add_product_to_showcase(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_showcase = Showcase.objects.all().get(sku=detail)
    selected_product = Product.objects.all().get(id=index)

    if not selected_showcase.product.all().filter(sku=selected_product.sku).exists():
        selected_showcase.product.add(selected_product)

    return {
        'url': url,
    }

def remove_product_from_showcase(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_showcase = Showcase.objects.all().get(sku=detail)
    selected_product = Product.objects.all().get(id=index)

    selected_showcase.product.remove(selected_product)

    return {
        'url': url,
    }

# ------------------ category
def edit_directory(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        root_directories = Directory.objects.all()
    except Directory.objects.all().DoesNotExist:
        raise Http404("No root directories")

    if not detail =='new':
        try:
            selected_root_directory = Directory.objects.all().get(sku=detail)
        except Directory.objects.all().DoesNotExist:
            raise Http404("No root directories")
    else:
        selected_root_directory = None

    if not selected_root_directory:
        sku = serial_number_generator(10).upper()
        if root_directories:
            rank = root_directories.count() + 1
        else:
            rank = 1
        selected_root_directory = Directory(rank=rank,
                                            sku=sku,
                                            )
        selected_root_directory.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        offer_en_title = request.POST.get('offer_en_title', False)
        offer_fr_title = request.POST.get('offer_fr_title', False)
        offer_ar_title = request.POST.get('offer_ar_title', False)
        offer_link = request.POST.get('offer_link', False)
        offer_price = request.POST.get('offer_price', False)
        thumb = request.FILES.get('thumb', False)


        if en_title:
            selected_root_directory.en_title = en_title

        if fr_title:
            selected_root_directory.fr_title = fr_title

        if ar_title:
            selected_root_directory.ar_title = ar_title

        if offer_en_title:
            selected_root_directory.offer_en_title = offer_en_title

        if offer_fr_title:
            selected_root_directory.offer_fr_title = offer_fr_title

        if offer_ar_title:
            selected_root_directory.offer_ar_title = offer_ar_title

        if offer_link:
            selected_root_directory.offer_link = offer_link

        if offer_price:
            selected_root_directory.offer_price = int(offer_price)

        if thumb:
            selected_root_directory.thumb = thumb

        selected_root_directory.save()

    return {
        'url': url,
    }

def add_category_to_directory(detail, index):
    url = "/shop-manager/e-shop.html"

    selected_directory = Directory.objects.all().get(sku=detail)
    selected_category = Category.objects.all().get(id=index)

    if not selected_directory.category.all().filter(sku=selected_category.sku).exists():
        selected_directory.category.add(selected_category)

    return {
        'url': url,
    }

def remove_category_from_directory(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_directory = Directory.objects.all().get(sku=detail)
    selected_category = Category.objects.all().get(id=index)

    selected_directory.category.remove(selected_category)

    return {
        'url': url,
    }

def edit_category(request, detail):
    url = "/shop-manager/e-shop.html"
    try:
        categories = Category.objects.all()
    except Category.objects.all().DoesNotExist:
        raise Http404("No categories")

    if not detail =='new':
        try:
            selected_category = Category.objects.all().get(sku=detail)
        except Category.objects.all().DoesNotExist:
            raise Http404("No category")
    else:
        selected_category = None

    if not selected_category:
        sku = serial_number_generator(10).upper()
        if categories:
            rank = categories.count() + 1
        else:
            rank = 1
        selected_category = Category(rank=rank,
                                     sku=sku,
                                     )
        selected_category.save()

    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        thumb = request.FILES.get('thumb', False)


        if en_title:
            selected_category.en_title = en_title

        if fr_title:
            selected_category.fr_title = fr_title

        if ar_title:
            selected_category.ar_title = ar_title

        if thumb:
            selected_category.thumb = thumb

        selected_category.save()

    return {
        'url': url,
    }

def add_product_to_category(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_category = Category.objects.all().get(sku=detail)
    selected_product = Product.objects.all().get(id=index)

    if not selected_category.product.all().filter(sku=selected_product.sku).exists():
        selected_category.product.add(selected_product)

    return {
        'url': url,
    }

def remove_product_from_category(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_category = Category.objects.all().get(sku=detail)
    selected_product = Product.objects.all().get(id=index)

    selected_category.product.remove(selected_product)

    return {
        'url': url,
    }


def up_category(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_category = Category.objects.all().get(sku=detail)
    max_rank = Category.objects.all().count()

    if index == max_rank:
        next_category = Category.objects.all().get(rank=1)
    else:
        next_category = Category.objects.all().get(rank=index + 1)

    selected_category.rank = next_category.rank
    next_category.rank = index

    selected_category.save()
    next_category.save()

    return {
        'url': url,
    }

def down_category(detail, index):
    url = "/shop-manager/e-shop.html"
    selected_category = Category.objects.all().get(sku=detail)
    max_rank = Category.objects.all().count()

    if index == 1:
        next_category = Category.objects.all().get(rank=max_rank)
    else:
        next_category = Category.objects.all().get(rank=index - 1)

    selected_category.rank = next_category.rank
    next_category.rank = index

    selected_category.save()
    next_category.save()

    return {
        'url': url,
    }





# ------------------ functions
def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str