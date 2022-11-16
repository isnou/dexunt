import random
import string
from .models import InventoryProduct


def add_new_product(request, action):
    if action == "en_add_new_product":
        url = "ltr/shop-manager/add-product.html"
        lang = "en"
    elif action == 'en_save_general_product_information':
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
        prog = 0
        if request.method == 'POST':
            product_name = request.POST.get('product_name', False)
            buy_price = request.POST.get('buy_price', False)
            if buy_price:
                prog += 1
            quantity = int(request.POST.get('quantity', False))
            thumb = request.FILES.get('thumb', False)
            if thumb:
                prog += 1
            upc = request.POST.get('upc', False)
            if upc:
                new_product = InventoryProduct(product_name=product_name,
                                               upc=upc,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.sku = serial_number_generator(9).upper()
                new_product.profile += prog + 1
                new_product.save()
            else:
                new_product = InventoryProduct(product_name=product_name,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.sku = serial_number_generator(9).upper()
                new_product.profile += prog
                new_product.save()
    else:
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
    result = {
        'url': url,
        'lang': lang,
    }
    return result


def edit(request, action, sku):
    all_products = InventoryProduct.objects.all()
    product_to_edit = all_products.get(sku=sku)
    if action == "en_product_edit":
        url = "ltr/shop-manager/edit-product.html"
        lang = "en"
    elif action == 'en_product_save':
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
        prog = 0
        if request.method == 'POST':
            product_to_edit.product_name = request.POST.get('product_name', False)
            product_to_edit.buy_price = int(request.POST.get('buy_price', False))
            if buy_price > 0:
                prog += 1
            product_to_edit.quantity = int(request.POST.get('quantity', False))
            product_to_edit.thumb = request.FILES.get('thumb', False)
            if thumb:
                prog += 1
            product_to_edit.upc = request.POST.get('upc', False)
            if upc != 'NOBARCODE':
                new_product.profile += prog + 1
                new_product.save()
            else:
                new_product = InventoryProduct(product_name=product_name,
                                               buy_price=buy_price,
                                               quantity=quantity,
                                               thumb=thumb,
                                               )
                new_product.sku = serial_number_generator(9).upper()
                new_product.profile += prog
                new_product.save()
    else:
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
    result = {
        'url': url,
        'lang': lang,
        'product_to_edit': product_to_edit
    }
    return result


def delete(request, action, sku):
    if action == "ar_product_delete":
        url = "rtl/shop-manager/inventory.html"
        lang = "ar"
    elif action == 'en_product_delete':
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
        all_products = InventoryProduct.objects.all()
        selected_product = all_products.get(sku=sku)
        selected_product.delete()
    else:
        url = "ltr/shop-manager/inventory.html"
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
