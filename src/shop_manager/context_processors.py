from .models import Product


def shop_manager_content(request):
    try:
        raw_products_list = Product.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    products = raw_products_list.order_by('en_product_title', 'en_variant', 'updated_at')
    inventory_product_count = raw_products_list.count()
    showcase_products = raw_products_list.filter(type='main')
    return {
        'products': products,
        'inventory_product_count': inventory_product_count,
        'showcase_products': showcase_products,
        'fool': [0, 1, 2, 3, 4],
    }
