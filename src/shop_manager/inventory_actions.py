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

    return {
        'url': url,
    }


def edit(request, sku):
    url = "shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    token_variant = selected_product.en_variant
    token_en_product_title = selected_product.en_product_title
    if request.method == 'POST':
        en_product_title = request.POST.get('en_product_title', False)
        if en_product_title:
            selected_product.en_product_title = en_product_title
            products = Product.objects.all().filter(en_product_title=token_en_product_title)
            for product in products:
                product.en_product_title = selected_product.en_product_title
                product.save()
        en_variant = request.POST.get('en_variant', False)
        if en_variant:
            selected_product.en_variant = en_variant
            sizes = Product.objects.all().filter(en_product_title=selected_product.en_product_title) \
                .filter(en_variant=token_variant).filter(type='size')
            for product in sizes:
                product.en_variant = selected_product.en_variant
                product.save()
        fr_product_title = request.POST.get('fr_product_title', False)
        if fr_product_title:
            selected_product.fr_product_title = fr_product_title
        fr_variant = request.POST.get('fr_variant', False)
        if fr_variant:
            selected_product.fr_variant = fr_variant
        ar_product_title = request.POST.get('ar_product_title', False)
        if ar_product_title:
            selected_product.ar_product_title = ar_product_title
        ar_variant = request.POST.get('ar_variant', False)
        if ar_variant:
            selected_product.ar_variant = ar_variant
        brand = request.POST.get('brand', False)
        if brand:
            selected_product.brand = brand
        model = request.POST.get('model', False)
        if model:
            selected_product.model = model
        upc = request.POST.get('upc', False)
        if upc:
            selected_product.upc = upc
        tag = request.POST.get('tag', False)
        if tag:
            selected_product.tag = tag
        quantity = request.POST.get('quantity', False)
        if quantity:
            selected_product.quantity = quantity
        buy_price = request.POST.get('buy_price', False)
        if buy_price:
            selected_product.buy_price = buy_price
        sell_price = request.POST.get('sell_price', False)
        if sell_price:
            selected_product.sell_price = sell_price
        discount_price = request.POST.get('discount_price', False)
        if discount_price:
            selected_product.discount_price = discount_price
    selected_product.save()

    return {
        'url': url,
    }


def add_new_photo(request, sku):
    url = "shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        photo = request.FILES.get('photo', False)
        new_product = Product(en_product_title=selected_product.en_product_title,
                              en_variant=selected_product.en_variant + ' photo',
                              thumb=photo,
                              )
        new_product.sku = serial_number_generator(9).upper()
        new_product.type = 'photo'
        new_product.save()

    return {
        'url': url,
    }


def edit_photo(request, sku):
    url = "shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        photo = request.FILES.get('photo', False)
        selected_product.thumb = photo
        selected_product.save()
    return {
        'url': url,
    }


def add_new_size(request, sku):
    url = "shop-manager/inventory-edit.html"
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
                              en_variant=selected_product.en_variant + ' size',
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

    return {
        'url': url,
    }


def add_a_set(request, sku):
    url = "shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        en_variant = request.POST.get('en_variant', False)
        fr_variant = request.POST.get('fr_variant', False)
        ar_variant = request.POST.get('ar_variant', False)
        if selected_product.fr_product_title:
            fr_product_title = selected_product.fr_product_title
        else:
            fr_product_title = None
        if selected_product.ar_product_title:
            ar_product_title = selected_product.ar_product_title
        else:
            ar_product_title = None
        if selected_product.brand:
            brand = selected_product.brand
        else:
            brand = None
        if selected_product.model:
            model = selected_product.model
        else:
            model = None
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
                              en_variant=en_variant + ' set',
                              fr_product_title=fr_product_title,
                              fr_variant=fr_variant,
                              ar_product_title=ar_product_title,
                              ar_variant=ar_variant,
                              brand=brand,
                              model=model,
                              upc=upc,
                              tag=selected_product.tag,
                              quantity=int(quantity),
                              buy_price=int(buy_price),
                              sell_price=int(sell_price),
                              discount_price=int(discount_price),
                              thumb=thumb,
                              )
        new_product.sku = serial_number_generator(9).upper()
        new_product.type = 'set'
        new_product.save()

    return {
        'url': url,
    }


def edit_a_set(request, sku):
    url = "shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        en_variant = request.POST.get('en_variant', False)
        if en_variant:
            selected_product.en_variant = en_variant + ' set'
        fr_variant = request.POST.get('fr_variant', False)
        if fr_variant:
            selected_product.fr_variant = fr_variant
        ar_variant = request.POST.get('ar_variant', False)
        if ar_variant:
            selected_product.ar_variant = ar_variant
        upc = request.POST.get('upc', False)
        if upc:
            selected_product.upc = upc
        quantity = request.POST.get('quantity', False)
        if quantity:
            selected_product.quantity = quantity
        buy_price = request.POST.get('buy_price', False)
        if buy_price:
            selected_product.buy_price = buy_price
        sell_price = request.POST.get('sell_price', False)
        if sell_price:
            selected_product.sell_price = sell_price
        discount_price = request.POST.get('discount_price', False)
        if discount_price:
            selected_product.discount_price = discount_price
    selected_product.save()

    return {
        'url': url,
    }


def add_new_feature(request, sku):
    url = "shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        en_title = request.POST.get('en_feature_title', False)
        en_value = request.POST.get('en_feature_value', False)
        fr_title = request.POST.get('fr_feature_title', False)
        fr_value = request.POST.get('fr_feature_value', False)
        ar_title = request.POST.get('ar_feature_title', False)
        ar_value = request.POST.get('ar_feature_value', False)
        feature = Feature(en_title=en_title,
                          en_value=en_value,
                          fr_title=fr_title,
                          fr_value=fr_value,
                          ar_title=ar_title,
                          ar_value=ar_value,
                          )
        feature.save()
        selected_product.features.add(feature)
        selected_product.save()

    return {
        'url': url,
    }


def edit_feature(request, identity):
    url = "shop-manager/inventory-edit.html"
    selected_feature = Feature.objects.all().get(id=identity)
    if request.method == 'POST':
        en_title = request.POST.get('en_feature_title', False)
        if en_title:
            selected_feature.en_title = en_title
        en_value = request.POST.get('en_feature_value', False)
        if en_value:
            selected_feature.en_value = en_value
        fr_title = request.POST.get('fr_feature_title', False)
        if fr_title:
            selected_feature.fr_title = fr_title
        fr_value = request.POST.get('fr_feature_value', False)
        if fr_value:
            selected_feature.fr_value = fr_value
        ar_title = request.POST.get('ar_feature_title', False)
        if ar_title:
            selected_feature.ar_title = ar_title
        ar_value = request.POST.get('ar_feature_value', False)
        if ar_value:
            selected_feature.ar_value = ar_value

        selected_feature.save()

    return {
        'url': url,
    }


def add_quantity(request, sku):
    url = "shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_product.quantity += 1
    selected_product.save()
    result = {
        'url': url,
    }
    return result


def remove_quantity(request, sku):
    url = "shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    if selected_product.quantity > 0:
        selected_product.quantity -= 1
    else:
        selected_product.quantity = 0
    selected_product.save()
    result = {
        'url': url,
    }
    return result


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
