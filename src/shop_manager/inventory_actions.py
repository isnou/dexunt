import random
import string
from django.db import models
from .models import InventoryProduct, ProductAlbum, InventoryProductFeatures


def add_new_product(request):
    url = "ltr/shop-manager/inventory.html"
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
    result = {
        'url': url,
        'lang': lang,
    }
    return result


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
