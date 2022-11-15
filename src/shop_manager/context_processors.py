from .models import InventoryProduct


def shop_manager_content(request):
    try:
        products = InventoryProduct.objects.all()
    except InventoryProduct.DoesNotExist:
        raise Http404("No products")
    return {
        'products': products,
        'fool': [0, 1, 2, 3, 4],
    }
