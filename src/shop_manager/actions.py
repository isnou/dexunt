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
        if request.method == 'POST':
            product_name = request.POST.get('product_name', False)
            buy_price = request.POST.get('buy_price', False)
            if not buy_price:
                buy_price = 0
            quantity = int(request.POST.get('quantity', False))
            thumb = request.FILES.get('thumb', False)
            upc = request.POST.get('upc', False)
            new_product = InventoryProduct(product_name=product_name,
                                           buy_price=int(buy_price),
                                           quantity=quantity,
                                           thumb=thumb,
                                           )
            if upc:
                new_product.upc = upc
            new_product.profile = 1
            if new_product.upc:
                new_product.profile += 1
            if new_product.thumb:
                new_product.profile += 1
            if new_product.buy_price > 0:
                new_product.profile += 1
            new_product.sku = serial_number_generator(9).upper()
            new_product.save()
    else:
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
    result = {
        'url': url,
        'lang': lang,
    }
    return result


def view(request, action, sku):
    all_products = InventoryProduct.objects.all()
    product_to_view = all_products.get(sku=sku)
    features = product_to_view.features.all()
    photos = product_to_view.album.all()
    if action == "en_product_view":
        url = "ltr/shop-manager/view-product.html"
        lang = "en"
    else:
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
    result = {
        'url': url,
        'lang': lang,
        'features': features,
        'photos': photos,
        'product_to_view': product_to_view
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
        if request.method == 'POST':
            product_name = request.POST.get('product_name', False)
            if product_name:
                product_to_edit.product_name = product_name
            buy_price = request.POST.get('buy_price', False)
            if buy_price:
                product_to_edit.buy_price = int(buy_price)
            quantity = request.POST.get('quantity', False)
            if quantity:
                product_to_edit.quantity = int(quantity)
            thumb = request.FILES.get('thumb', False)
            if thumb:
                product_to_edit.thumb = thumb
            else:
                product_to_edit.delete(thumb)
            upc = request.POST.get('upc', False)
            if upc:
                product_to_edit.upc = upc
            product_to_edit.profile = 1
            if product_to_edit.upc:
                product_to_edit.profile += 1
            if product_to_edit.thumb:
                product_to_edit.profile += 1
            if product_to_edit.buy_price > 0:
                product_to_edit.profile += 1
        product_to_edit.save()
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
