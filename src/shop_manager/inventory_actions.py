import random
import string
from .models import Product, Feature


def add_new_product(request):
    url = "shop-manager/inventory.html"
    if request.method == 'POST':
        en_product_title = request.POST.get('en_product_title', False)
        en_variant = request.POST.get('en_variant', False)
        fr_product_title = request.POST.get('fr_product_title', False)
        fr_variant = request.POST.get('fr_variant', False)
        ar_product_title = request.POST.get('ar_product_title', False)
        ar_variant = request.POST.get('ar_variant', False)
        brand = request.POST.get('brand', False)
        model = request.POST.get('model', False)
        upc = request.POST.get('upc', False)
        if not upc:
            upc = serial_number_generator(12).upper()
        tag = request.POST.get('tag', False)
        quantity = request.POST.get('quantity', False)
        if not quantity:
            quantity = 0
        buy_price = request.POST.get('buy_price', False)
        if not buy_price:
            buy_price = 0
        sell_price = request.POST.get('sell_price', False)
        if not sell_price:
            sell_price = 0
        discount_price = request.POST.get('discount_price', False)
        if not discount_price:
            discount_price = 0
        thumb = request.FILES.get('thumb', False)
        new_product = Product(en_product_title=en_product_title,
                              en_variant=en_variant,
                              fr_product_title=fr_product_title,
                              fr_variant=fr_variant,
                              ar_product_title=ar_product_title,
                              ar_variant=ar_variant,
                              brand=brand,
                              model=model,
                              upc=upc,
                              tag=tag,
                              quantity=int(quantity),
                              buy_price=int(buy_price),
                              sell_price=int(sell_price),
                              discount_price=int(discount_price),
                              thumb=thumb,
                              )
        new_product.sku = serial_number_generator(9).upper()
        new_product.type = 'main'
        new_product.save()
    result = {
        'url': url,
    }
    return result


def add_new_photo(request, sku):
    url = "shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        thumb = request.FILES.get('thumb', False)
        new_product = Product(en_product_title=selected_product.en_product_title,
                              en_variant=selected_product.en_variant,
                              thumb=thumb,
                              )
        new_product.sku = serial_number_generator(9).upper()
        new_product.save()
    result = {
        'url': url,
    }
    return result


def add_new_size(request, sku):
    url = "shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        size = request.POST.get('size', False)
        upc = request.POST.get('upc', False)
        if not upc:
            upc = serial_number_generator(12).upper()
        quantity = request.POST.get('quantity', False)
        if not quantity:
            quantity = selected_product.quantity
        buy_price = request.POST.get('buy_price', False)
        if not buy_price:
            buy_price = selected_product.buy_price
        sell_price = request.POST.get('sell_price', False)
        if not sell_price:
            sell_price = selected_product.sell_price
        discount_price = request.POST.get('discount_price', False)
        if not discount_price:
            discount_price = selected_product.discount_price
        new_product = Product(en_product_title=selected_product.en_product_title,
                              en_variant=selected_product.en_variant,
                              upc=upc,
                              size=size,
                              quantity=int(quantity),
                              buy_price=int(buy_price),
                              sell_price=int(sell_price),
                              discount_price=int(discount_price),
                              )
        new_product.sku = serial_number_generator(9).upper()
        new_product.type = 'size'
        new_product.save()
    result = {
        'url': url,
    }
    return result


def add_new_variant(request, sku):
    url = "shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        en_variant = request.POST.get('en_variant', False)
        fr_variant = request.POST.get('fr_variant', False)
        ar_variant = request.POST.get('ar_variant', False)
        upc = request.POST.get('upc', False)
        if not upc:
            upc = serial_number_generator(12).upper()
        quantity = request.POST.get('quantity', False)
        if not quantity:
            quantity = selected_product.quantity
        buy_price = request.POST.get('buy_price', False)
        if not buy_price:
            buy_price = selected_product.buy_price
        sell_price = request.POST.get('sell_price', False)
        if not sell_price:
            sell_price = selected_product.sell_price
        discount_price = request.POST.get('discount_price', False)
        if not discount_price:
            discount_price = selected_product.discount_price
        thumb = request.FILES.get('thumb', False)
        new_product = Product(en_product_title=selected_product.en_product_title,
                              en_variant=en_variant,
                              fr_variant=fr_variant,
                              ar_variant=ar_variant,
                              upc=upc,
                              quantity=int(quantity),
                              buy_price=int(buy_price),
                              sell_price=int(sell_price),
                              discount_price=int(discount_price),
                              thumb=thumb,
                              )
        new_product.sku = serial_number_generator(9).upper()
        new_product.type = 'variant'
        new_product.save()
    result = {
        'url': url,
    }
    return result


def add_features(request, language, sku):
    url = "shop-manager/inventory-product.html"
    selected_product = Product.objects.all().get(sku=sku)
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
    selected_product = Product.objects.all().get(sku=sku)
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
        if selected_product.profile < 3:
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
    selected_product = Product.objects.all().get(sku=sku)
    if photos_count < 4:
        photos_progress = photos_count
    else:
        photos_progress = 4
    if features_count < 4:
        features_progress = features_count
    else:
        features_progress = 4
    selected_product.profile = 2 + photos_progress + features_progress
    selected_product.save()
    return selected_product


def new_feature(feature_name, feature_value, language):
    feature = ProductFeatures()
    feature.language = language
    feature.type = feature_name
    feature.value = feature_value
    feature.save()
    return feature


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
