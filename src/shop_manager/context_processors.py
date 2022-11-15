from .models import InventoryProduct


def shop_manager_content(request):
    products = InventoryProduct.objects.all()
    return products
