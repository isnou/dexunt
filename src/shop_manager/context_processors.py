from .models import Product


def shop_manager_content(request):

    try:
        all_products = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No products")

    published_products = all_products.exclude(publish=False)
    best_sellers = published_products.order_by('-sell_rate')[:4]
    top_rated = published_products.order_by('-review_rate')[:4]
    new_arrivals = published_products.order_by('-created_at')[:4]

    return {
        'all_products' : all_products,
        'best_sellers' : best_sellers,
        'top_rated' : top_rated,
        'new_arrivals' : new_arrivals,
    }
