from .models import Product


def shop_manager_content(request):
    try:
        raw_products_list = Product.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    inventory_products = raw_products_list.order_by('en_title')
    showcase_products = raw_products_list.exclude(publish=False)
    best_sellers = showcase_products.order_by('-sell_rate')[:4]
    top_rated = showcase_products.order_by('-review_rate')[:4]
    new_arrivals = showcase_products.order_by('-updated_at')[:4]
    return {
        'inventory_products': inventory_products,
        'showcase_products': showcase_products,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'new_arrivals': new_arrivals,
        'fool': [0, 1, 2, 3, 4],
    }
