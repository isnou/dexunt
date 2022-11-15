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
            upc = request.POST.get('upc', False)
            buy_price = request.POST.get('buy_price', False)
            quantity = request.POST.get('quantity', False)
            thumb = request.POST.get('thumb', False)
            new_product = InventoryProduct(product_name=product_name,
                                           upc=upc,
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
