import random
import string
from .models import InventoryProduct, ProductAlbum, InventoryProductFeatures


def add_new_product(request):
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
        new_product.profile = 0
        if new_product.upc:
            new_product.profile += 1
        if new_product.buy_price > 0:
            new_product.profile += 1
        new_product.save()
    result = {
        'url': url,
    }
    return result


def add_new_photo(request, sku):
    url = "shop-manager/inventory-product.html"
    selected_product = InventoryProduct.objects.all().get(sku=sku)
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


def add_features(request, language, sku):
    url = "shop-manager/inventory-product.html"
    selected_product = InventoryProduct.objects.all().get(sku=sku)
    if request.method == 'POST':
        model = request.POST.get('model', False)
        if model:
            if selected_product.features.all().filter(type='model').exists():
                selected_product.features.all().filter(type='model', language=language).delete()
            selected_product.features.add(new_feature('model', model, language))
        brand = request.POST.get('brand', False)
        if brand:
            if selected_product.features.all().filter(type='brand').exists():
                selected_product.features.all().filter(type='brand', language=language).delete()
            selected_product.features.add(new_feature('brand', brand, language))
        color = request.POST.get('color', False)
        if color:
            if selected_product.features.all().filter(type='color').exists():
                selected_product.features.all().filter(type='color', language=language).delete()
            selected_product.features.add(new_feature('color', color, language))
        dimensions = request.POST.get('dimensions', False)
        if dimensions:
            if selected_product.features.all().filter(type='dimensions').exists():
                selected_product.features.all().filter(type='dimensions', language=language).delete()
            selected_product.features.add(new_feature('dimensions', dimensions, language))
        size = request.POST.get('size', False)
        if size:
            if selected_product.features.all().filter(type='size').exists():
                selected_product.features.all().filter(type='size', language=language).delete()
            selected_product.features.add(new_feature('size', size, language))
        weight = request.POST.get('weight', False)
        if weight:
            if selected_product.features.all().filter(type='weight').exists():
                selected_product.features.all().filter(type='weight', language=language).delete()
            selected_product.features.add(new_feature('weight', weight, language))
    selected_product.save()
    result = {
        'url': url,
    }
    return result


def edit(request, sku):
    url = "shop-manager/inventory-product.html"
    selected_product = InventoryProduct.objects.all().get(sku=sku)
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
        selected_product.profile = 0
        if selected_product.upc:
            selected_product.profile += 1
        if selected_product.buy_price > 0:
            selected_product.profile += 1
        selected_product.save()
    result = {
        'url': url,
    }
    return result


def progress_counter(sku, photos_count, features_count):
    selected_product = InventoryProduct.objects.all().get(sku=sku)
    if photos_count < 4:
        photos_progress = photos_count
    else:
        photos_progress = 4
    if features_count < 4:
        features_progress = features_count
    else:
        features_progress = 4
    selected_product = 2 + photos_progress + features_progress
    selected_product.save()


def new_feature(feature_name, feature_value, language):
    feature = InventoryProductFeatures()
    feature.language = language
    feature.type = feature_name
    feature.value = feature_value
    feature.save()
    return feature


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
