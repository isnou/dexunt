from .models import Product


def shop_manager_content(request):
    try:
        raw_products_list = Product.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    products = raw_products_list.order_by('en_product_title', 'attach')
    inventory_product_count = raw_products_list.count()
    collection = raw_products_list.exclude(type='set').exclude(type='photo').exclude(type='size')
    showcase_products = collection.order_by('-updated_at')
    best_sellers = collection.order_by('-sell_rate')[:4]
    top_rated = collection.order_by('-review_rate')[:4]
    new_arrivals = collection.order_by('-created_at')[:4]
    return {
        'products': products,
        'inventory_product_count': inventory_product_count,
        'showcase_products': showcase_products,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'new_arrivals': new_arrivals,
        'fool': [0, 1, 2, 3, 4],
    }
