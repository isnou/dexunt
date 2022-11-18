import random
import string
from .models import InventoryProduct, ProductAlbum, InventoryProductFeatures


def add_new_product(request, lang):
    url = "shop-manager/inventory.html"
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
        new_product.sku = serial_number_generator(9).upper()
        new_product.profile = 1
        if new_product.upc:
            new_product.profile += 1
        if new_product.buy_price > 0:
            new_product.profile += 1
        new_product.save()
    result = {
        'url': url,
    }
    return result


def add_new_photo(request, lang, sku):
    url = "shop-manager/inventory-product.html"
    all_products = InventoryProduct.objects.all()
    selected_product = all_products.get(sku=sku)
    if request.method == 'POST':
        image_to_add = request.FILES.get('image_to_add', False)
        if image_to_add:
            photo = ProductAlbum(
                file_name=selected_product.product_name,
                picture=image_to_add,
            )
            photo.save()
            selected_product.album.add(photo)
    selected_product.save()
    result = {
        'url': url,
    }
    return result


def edit(request, lang, sku):
    url = "shop-manager/inventory-product.html"
    all_products = InventoryProduct.objects.all()
    selected_product = all_products.get(sku=sku)
    if request.method == 'POST':
        product_name = request.POST.get('product_name', False)
        if product_name:
            selected_product.product_name = product_name
        buy_price = request.POST.get('buy_price', False)
        if buy_price:
            selected_product.buy_price = int(buy_price)
        quantity = request.POST.get('quantity', False)
        if quantity:
            selected_product.quantity = int(quantity)
        thumb = request.FILES.get('thumb', False)
        if thumb:
            selected_product.thumb = thumb
        upc = request.POST.get('upc', False)
        if upc:
            selected_product.upc = upc
        selected_product.profile = 1
        if selected_product.upc:
            selected_product.profile += 1
        if selected_product.buy_price > 0:
            selected_product.profile += 1
        selected_product.save()
    result = {
        'url': url,
    }
    return result


def delete_product(request, lang, sku):
    url = "shop-manager/inventory.html"
    all_products = InventoryProduct.objects.all()
    selected_product = all_products.get(sku=sku)
    selected_product.delete()
    result = {
        'url': url,
    }
    return result


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
