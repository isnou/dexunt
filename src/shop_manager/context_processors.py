from .models import Product


def shop_manager_content(request):
    try:
        raw_products_list = Product.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    products = raw_products_list.order_by('en_product_title', 'en_variant', '-updated_at')
    inventory_product_count = raw_products_list.count()
    showcase_products = raw_products_list.filter(type='main') + raw_products_list.filter(type='proto')
    best_sellers = raw_products_list.filter(type='main').filter(type='proto').order_by('-sell_rate')[:4]
    top_rated = raw_products_list.filter(type='main').filter(type='proto').order_by('-review_rate')[:4]
    new_arrivals = raw_products_list.filter(type='main').filter(type='proto').order_by('-created_at')[:4]
    return {
        'products': products,
        'inventory_product_count': inventory_product_count,
        'showcase_products': showcase_products,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'new_arrivals': new_arrivals,
        'fool': [0, 1, 2, 3, 4],
    }
