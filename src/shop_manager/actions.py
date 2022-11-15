from .models import InventoryProduct


def add_product_actions(request, action):
    if action == "ar":
        url = "rtl/shop-manager/add-product.html"
        lang = "ar"
    elif action == 'en_save_general_product_information':
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
        if request.method == 'POST':
            product_name = request.POST.get('product_name', False)

            buy_price = request.POST.get('buy_price', False)
            quantity = request.POST.get('quantity', False)
            thumb = request.FILES.get('thumb', False)
            upc = request.POST.get('upc', False)
            if upc != 0:
                new_product = InventoryProduct(product_name=product_name,
                                               upc=upc,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.save()
            else:
                new_product = InventoryProduct(product_name=product_name,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.save()
    else:
        url = "ltr/shop-manager/add-product.html"
        lang = "en"
    result = {
        'url': url,
        'lang': lang,
    }
    return result
