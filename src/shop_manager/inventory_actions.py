import random
import string
from .models import Product, Feature, Album, Collection


# ------------------ inventory
def add_new_product(request):
    url = "/shop-manager/inventory.html"
    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        en_variant = request.POST.get('en_variant', False)
        fr_title = request.POST.get('fr_title', False)
        fr_variant = request.POST.get('fr_variant', False)
        ar_title = request.POST.get('ar_title', False)
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
        new_product = Product(en_title=en_title,
                              en_variant=en_variant,
                              fr_title=fr_title,
                              fr_variant=fr_variant,
                              ar_title=ar_title,
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
        new_product.sku = serial_number_generator(10).upper()
        new_product.publish = True
        new_product.type = 'main'
        new_product.save()
        Collection(en_title=new_product.en_title, ).save().product.add(new_product).save()

    return {
        'url': url,
    }


def add_new_variant(request, sku):
    url = "/shop-manager/inventory.html"
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
                              en_variant=en_variant,
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
        new_product.sku = serial_number_generator(10).upper()
        new_product.attach = serial_number_generator(10).upper()
        new_product.type = 'variant'
        new_product.save()

    return {
        'url': url,
    }


def add_quantity(sku):
    url = "/shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_product.quantity += 1
    selected_product.save()
    result = {
        'url': url,
    }
    return result


def remove_quantity(sku):
    url = "/shop-manager/inventory.html"
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


# ------------------ inventory edit
def edit_product(request, sku):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)

    if request.method == 'POST':
        thumb = request.FILES.get('thumb', False)
        if thumb:
            selected_product.thumb = thumb
        en_title = request.POST.get('en_title', False)
        if en_title:
            selected_product.en_title = en_title
        en_variant = request.POST.get('en_variant', False)
        if en_variant:
            selected_product.en_variant = en_variant

        fr_title = request.POST.get('fr_title', False)
        if fr_title:
            selected_product.fr_title = fr_title
        fr_variant = request.POST.get('fr_variant', False)
        if fr_variant:
            selected_product.fr_variant = fr_variant

        ar_title = request.POST.get('ar_title', False)
        if ar_title:
            selected_product.ar_title = ar_title
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
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        photo = request.FILES.get('photo', False)
        album = Album(file_name=selected_product.en_title,
                      image=photo,
                      )
        album.save()
        selected_product.album.add(album)
        selected_product.save()

    return {
        'url': url,
    }


def add_new_feature(request, sku):
    url = "/shop-manager/inventory-edit.html"
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


def edit_feature(request, index):
    url = "/shop-manager/inventory-edit.html"
    selected_feature = Feature.objects.all().get(id=index)
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


def add_new_size(request, sku):
    url = "/shop-manager/inventory-edit.html"
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
        new_product.sku = serial_number_generator(10).upper()
        new_product.attach = selected_product.attach
        new_product.type = 'size'
        new_product.save()

        quantity = 0
        attached_products = Product.objects.all().filter(attach=selected_product.attach).exclude(sku=sku)
        for attached_product in attached_products:
            quantity += attached_product.quantity
        selected_product.quantity = quantity

        if selected_product.type == 'main':
            selected_product.type = 'proto'
        if selected_product.type == 'variant':
            selected_product.type = 'proto_variant'
        if quantity == 0:
            if selected_product.type == 'proto':
                selected_product.type = 'main'
            if selected_product.type == 'proto_variant':
                selected_product.type = 'variant'

        selected_product.save()

    return {
        'url': url,
    }


def edit_size(request, sku):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    attached_products = Product.objects.all().filter(attach=selected_product.attach)
    if attached_products.filter(type='proto').exists():
        main_product = attached_products.get(type='proto')
        attached_products = attached_products.exclude(type='proto')
    elif attached_products.filter(type='proto_variant').exists():
        main_product = attached_products.get(type='proto_variant')
        attached_products = attached_products.exclude(type='proto_variant')
    else:
        main_product = None

    if request.method == 'POST':
        size = request.POST.get('size', False)
        if size:
            selected_product.size = size
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

        quantity = 0
        for attached_product in attached_products:
            quantity += attached_product.quantity
        main_product.quantity = quantity

        selected_product.save()
        main_product.save()

    return {
        'url': url,
        'sku': main_product.sku,
    }


def add_a_set(request, sku):
    url = "/shop-manager/inventory-edit.html"
    all_products = Product.objects.all()
    selected_product = all_products.get(sku=sku)

    if request.method == 'POST':
        en_variant = request.POST.get('en_variant', False)
        fr_variant = request.POST.get('fr_variant', False)
        ar_variant = request.POST.get('ar_variant', False)
        thumb = request.FILES.get('thumb', False)
        upc = request.POST.get('upc', False)
        if not upc:
            upc = serial_number_generator(12).upper()
        quantity = request.POST.get('quantity', False)
        if not quantity:
            quantity = 0
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
        new_product.sku = serial_number_generator(10).upper()
        new_product.attach = selected_product.attach
        new_product.type = 'set'
        new_product.save()

        if selected_product.type == 'main':
            selected_product.type = 'proto'
        if selected_product.type == 'variant':
            selected_product.type = 'proto_variant'

        selected_product.save()

    return {
        'url': url,
    }


def edit_a_set(request, sku):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    attached_products = Product.objects.all().filter(attach=selected_product.attach)
    if attached_products.filter(type='main').exists():
        main_product = attached_products.get(type='main')
    elif attached_products.filter(type='variant').exists():
        main_product = attached_products.get(type='variant')
    else:
        main_product = None

    if request.method == 'POST':
        en_variant = request.POST.get('en_variant', False)
        if en_variant:
            selected_product.en_variant = en_variant
        fr_variant = request.POST.get('fr_variant', False)
        if fr_variant:
            selected_product.fr_variant = fr_variant
        ar_variant = request.POST.get('ar_variant', False)
        if ar_variant:
            selected_product.ar_variant = ar_variant
        thumb = request.FILES.get('thumb', False)
        if thumb:
            selected_product.thumb = thumb
        size = request.POST.get('size', False)
        if size:
            selected_product.size = size
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
        'sku': main_product.sku,
    }


def delete_attached(sku, index):
    url = "/shop-manager/inventory-edit.html"
    all_products = Product.objects.all()
    if all_products.filter(sku=sku).exists():
        selected_product = all_products.get(sku=sku)
        attached_products = all_products.filter(attach=selected_product.attach).exclude(id=index).exclude(type='photo')
        main_product = all_products.get(id=index)

        selected_product.delete()

        quantity = 0
        for attached_product in attached_products:
            quantity += attached_product.quantity

        if not attached_products.count():
            if main_product.type == 'proto':
                main_product.type = 'main'
            if main_product.type == 'proto_variant':
                main_product.type = 'variant'

        main_product.quantity = quantity
        main_product.save()
    else:
        main_product = all_products.get(id=index)

    return {
        'url': url,
        'sku': main_product.sku,
    }


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
