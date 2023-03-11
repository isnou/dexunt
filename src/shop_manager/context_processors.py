from .models import Product, ShowcaseProduct


def shop_manager_content(request):
    try:
        shop_products_list = ShowcaseProduct.objects.all()
    except ShowcaseProduct.DoesNotExist:
        raise Http404("No products")

    try:
        all_products = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No products")

    products_to_publish = all_products.exclude(publish=False)
    best_sellers = products_to_publish.order_by('-sell_rate')[:4]
    top_rated = products_to_publish.order_by('-review_rate')[:4]
    new_arrivals = products_to_publish.order_by('-updated_at')[:4]
    return {
        'best_sellers' : best_sellers,
        'top_rated' : top_rated,
        'new_arrivals' : new_arrivals,
    }
