from .models import InventoryProduct


def shop_manager_content(request):
    try:
        products = InventoryProduct.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    inventory_product_count = products.count()
    return {
        'products': products,
        'inventory_product_count': inventory_product_count,
        'fool': [0, 1, 2, 3, 4],
    }
