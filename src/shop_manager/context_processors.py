from .models import Product


def shop_manager_content(request):
    try:
        raw_products_list = Product.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    products = raw_products_list.order_by('en_title')
    collection = raw_products_list.exclude(publish=False)
    showcase_products = collection.order_by('-updated_at')
    best_sellers = collection.order_by('-sell_rate')[:4]
    top_rated = collection.order_by('-review_rate')[:4]
    new_arrivals = collection.order_by('-created_at')[:4]
    return {
        'products': products,
        'showcase_products': showcase_products,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'new_arrivals': new_arrivals,
        'fool': [0, 1, 2, 3, 4],
    }
