import random
import string
from .models import InventoryProduct


def add_new_product(request, action):
    if action == "ar":
        url = "rtl/shop-manager/add-product.html"
        lang = "ar"
    elif action == 'en_save_general_product_information':
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
        prog = 0
        if request.method == 'POST':
            product_name = request.POST.get('product_name', False)
            buy_price = int(request.POST.get('buy_price', False))
            if buy_price > 0:
                prog += 1
            quantity = int(request.POST.get('quantity', False))
            thumb = request.FILES.get('thumb', False)
            if thumb:
                prog += 1
            upc = request.POST.get('upc', False)
            if upc != 'NOBARCODE':
                new_product = InventoryProduct(product_name=product_name,
                                               upc=upc,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.sku = serial_number_generator(4) + 'BRET'.upper()
                new_product.profile += prog + 1
                new_product.save()
            else:
                new_product = InventoryProduct(product_name=product_name,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.sku = serial_number_generator(4) + 'BRET'.upper()
                new_product.profile += prog
                new_product.save()
    else:
        url = "ltr/shop-manager/add-product.html"
        lang = "en"
    result = {
        'url': url,
        'lang': lang,
    }
    return result


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
