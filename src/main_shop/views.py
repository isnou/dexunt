from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import Product
from sell_manager.models import Clip
from .models import Layout


def main_shop_home(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"
    context = {
    }
    return render(request, url, context)


def change_language(request, language):
    if language == 'en':
        request.session['language'] = 'en'
    if language == 'fr':
        request.session['language'] = 'fr'
    if language == 'ar':
        request.session['language'] = 'ar'
    return redirect('main-shop-home')


def product(request, sku):
    try:
        clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No clips")

    if clips.filter(sku=sku).exists():
        clips = clips.filter(sku=sku)
        if clips.filter(type='points-products').exists():
            points_product = clips.get(type='points-products')
        else:
            points_product = None
        if clips.filter(type='delivery-products').exists():
            delivery_product = clips.get(type='delivery-products')
        else:
            delivery_product = None
        if clips.filter(type='solidarity-products').exists():
            solidarity_product = clips.get(type='solidarity-products')
        else:
            solidarity_product = None
    else:
        points_product = None
        delivery_product = None
        solidarity_product = None

    selected_product = Product.objects.all().get(sku=sku)
    related_products = Product.objects.all().filter(en_product_title=selected_product.en_product_title)
    selected_variants = related_products.filter(type='main').exclude(en_variant=selected_product.en_variant)

    album = related_products.filter(en_variant=selected_product.en_variant + ' photo')
    size_variants = related_products.filter(en_variant=selected_product.en_variant + ' size')

    direction = request.session.get('language')
    url = direction + "/main-shop/product.html"
    context = {
        'selected_product': selected_product,
        'selected_variants': selected_variants,
        'size_variants': size_variants,
        'album': album,
        'points_product': points_product,
        'delivery_product': delivery_product,
        'solidarity_product': solidarity_product,
    }
    return render(request, url, context)


def grid_shop(request, action, ref):
    all_showcases = Layout.objects.all().filter(type='showcase')
    products = Product.objects.all().filter(type='main')

    if all_showcases.filter(id=ref).exists():
        showcase = all_showcases.get(id=ref).prudcts.all()
    else:
        showcase = None

    if action == 'all':
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
        try:
            all_products = paginator.page(page)
        except PageNotAnInteger:
            all_products = paginator.page(1)
        except EmptyPage:
            all_products = paginator.page(paginator.num_pages)
        paginate_all = True
    else:
        all_products = products.all()[:4]
        paginate_all = False

    if action == 'showcase':
        page = request.GET.get('page', 1)
        paginator = Paginator(showcase, 4)
        try:
            showcase_products = paginator.page(page)
        except PageNotAnInteger:
            showcase_products = paginator.page(1)
        except EmptyPage:
            showcase_products = paginator.page(paginator.num_pages)
        paginate_showcase = True
    else:
        showcase_products = showcase.all()[:4]
        paginate_showcase = False

    direction = request.session.get('language')
    url = direction + "/main-shop/grid-shop.html"
    context = {
        'all_products': all_products,
        'paginate_all': paginate_all,
        'showcase_products': showcase_products,
        'paginate_showcase': paginate_showcase,
    }
    return render(request, url, context)
