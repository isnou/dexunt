from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import WhishedProducts


def all_products(request):
    url = "/main-shop/grid-shop.html"
    products = WhishedProducts.objects.all().exclude(type='variant').exclude(type='proto_variant').exclude(type='set')\
        .exclude(type='photo').exclude(type='size')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    return {
        'url': url,
        'products_list': products_list,
    }

def best_sellers(request):
    url = "/main-shop/grid-shop.html"
    products = WhishedProducts.objects.all().exclude(publish=False).order_by('-sell_rate')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    return {
        'url': url,
        'products_list': products_list,
    }

def new_arrivals(request):
    url = "/main-shop/grid-shop.html"
    products = WhishedProducts.objects.all().exclude(publish=False).order_by('-updated_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    return {
        'url': url,
        'products_list': products_list,
    }

def top_rated(request):
    url = "/main-shop/grid-shop.html"
    products = WhishedProducts.objects.all().exclude(publish=False).order_by('-review_rate')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    return {
        'url': url,
        'products_list': products_list,
    }


def showcase_products(request, ref):
    url = "/main-shop/grid-shop.html"
    products = Layout.objects.all().filter(type='showcase').get(id=ref).products.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    return {
        'url': url,
        'products_list': products_list,
    }
