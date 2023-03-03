import random
import string
from .models import Product, Feature, Album, Size


# ------------------ inventory
def add_new_product(request):
    url = "/shop-manager/inventory.html"
    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        en_spec = request.POST.get('en_spec', False)
        fr_spec = request.POST.get('fr_spec', False)
        ar_spec = request.POST.get('ar_spec', False)
        upc = request.POST.get('upc', False)
        tag = request.POST.get('tag', False)
        quantity = request.POST.get('quantity', False)
        buy_price = request.POST.get('buy_price', False)
        sell_price = request.POST.get('sell_price', False)
        discount_price = request.POST.get('discount_price', False)
        sku = serial_number_generator(10).upper()

        if not upc:
            upc = serial_number_generator(12).upper()
        if not quantity:
            quantity = 0
        if not buy_price:
            buy_price = 0
        if not sell_price:
            sell_price = 0
        if not discount_price:
            discount_price = 0

        Product(en_title=en_title,
                fr_title=fr_title,
                ar_title=ar_title,
                en_spec=en_spec,
                fr_spec=fr_spec,
                ar_spec=ar_spec,
                upc=upc,
                tag=tag,
                quantity=int(quantity),
                buy_price=int(buy_price),
                sell_price=int(sell_price),
                discount_price=int(discount_price),
                publish=True,
                sku=sku,
                ).save()

    return {
        'url': url,
    }


def add_new_variant(request, sku):
    url = "/shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_product_features = selected_product.features.all()
    if request.method == 'POST':
        en_variant = request.POST.get('en_variant', False)
        fr_variant = request.POST.get('fr_variant', False)
        ar_variant = request.POST.get('ar_variant', False)
        if selected_product.fr_title:
            fr_title = selected_product.fr_title
        else:
            fr_title = None
        if selected_product.ar_title:
            ar_title = selected_product.ar_title
        else:
            ar_title = None
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
        new_product = Product(en_title=selected_product.en_title,
                              en_variant=en_variant,
                              fr_title=fr_title,
                              fr_variant=fr_variant,
                              ar_title=ar_title,
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
                              attach=selected_product.attach
                              )
        new_product.sku = serial_number_generator(10).upper()
        new_product.publish = False
        new_product.type = 'main'
        new_product.save()
        Collection.objects.all().get(attach=new_product.attach).product.add(new_product)
        if selected_product_features.count():
            for selected_product_feature in selected_product_features:
                new_product.features.add(selected_product_feature)

    return {
        'url': url,
    }


def add_quantity(sku):
    url = "/shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_product.quantity += 1
    selected_product.save()

    return {
        'url': url,
    }


def remove_quantity(sku):
    url = "/shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    if selected_product.quantity > 0:
        selected_product.quantity -= 1
    else:
        selected_product.quantity = 0
    selected_product.save()

    return {
        'url': url,
    }


def publish(sku):
    url = "/shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_product.publish = True
    selected_product.save()

    return {
        'url': url,
    }


def unpublish(sku):
    url = "/shop-manager/inventory.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_product.publish = False
    selected_product.save()

    return {
        'url': url,
    }


# ------------------ inventory edit
def edit_product(request, sku):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        en_spec = request.POST.get('en_spec', False)
        fr_spec = request.POST.get('fr_spec', False)
        ar_spec = request.POST.get('ar_spec', False)
        upc = request.POST.get('upc', False)
        tag = request.POST.get('tag', False)
        quantity = request.POST.get('quantity', False)
        buy_price = request.POST.get('buy_price', False)
        sell_price = request.POST.get('sell_price', False)
        discount_price = request.POST.get('discount_price', False)

        if en_title:
            selected_product.en_title = en_title
        if fr_title:
            selected_product.fr_title = fr_title
        if ar_title:
            selected_product.ar_title = ar_title
        if en_spec:
            selected_product.en_spec = en_spec
        if fr_spec:
            selected_product.fr_spec = fr_spec
        if ar_spec:
            selected_product.ar_spec = ar_spec
        if upc:
            selected_product.upc = upc
        if tag:
            selected_product.tag = tag
        if quantity:
            selected_product.quantity = quantity
        if buy_price:
            selected_product.buy_price = buy_price
        if sell_price:
            selected_product.sell_price = sell_price
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
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        upc = request.POST.get('upc', False)
        quantity = request.POST.get('quantity', False)
        buy_price = request.POST.get('buy_price', False)
        sell_price = request.POST.get('sell_price', False)
        discount_price = request.POST.get('discount_price', False)
        sku = serial_number_generator(10).upper()

        if not upc:
            upc = serial_number_generator(12).upper()
        if not quantity:
            quantity = selected_product.quantity
        if not buy_price:
            buy_price = selected_product.buy_price
        if not sell_price:
            sell_price = selected_product.sell_price
        if not discount_price:
            discount_price = selected_product.discount_price

        new_size = Size(en_title=en_title,
                        fr_title=fr_title,
                        ar_title=ar_title,
                        upc=upc,
                        sku=sku,
                        quantity=int(quantity),
                        buy_price=int(buy_price),
                        sell_price=int(sell_price),
                        discount_price=int(discount_price),
                        show_thumb=False,
                        )
        new_size.save()
        selected_product.size.add(new_size)

        quantity = 0
        for selected_product_size in selected_product.size.all():
            quantity += selected_product_size.quantity
        selected_product.quantity = quantity
        selected_product.save()

    return {
        'url': url,
    }


def edit_size(request, sku, index):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_size = Size.objects.all().get(id=index)
    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        quantity = request.POST.get('quantity', False)
        buy_price = request.POST.get('buy_price', False)
        sell_price = request.POST.get('sell_price', False)
        discount_price = request.POST.get('discount_price', False)

        if en_title:
            selected_size.en_title = en_title
        if fr_title:
            selected_size.fr_title = fr_title
        if ar_title:
            selected_size.ar_title = ar_title
        if quantity:
            selected_size.quantity = quantity
        if buy_price:
            selected_size.buy_price = buy_price
        if sell_price:
            selected_size.sell_price = sell_price
        if discount_price:
            selected_size.discount_price = discount_price

        selected_size.save()

        quantity = 0
        for selected_product_size in selected_product.size.all():
            quantity += selected_product_size.quantity
        selected_product.quantity = quantity
        selected_product.save()

    return {
        'url': url,
    }


def add_thumbnail_size(request, sku):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        upc = request.POST.get('upc', False)
        quantity = request.POST.get('quantity', False)
        buy_price = request.POST.get('buy_price', False)
        sell_price = request.POST.get('sell_price', False)
        discount_price = request.POST.get('discount_price', False)
        thumb = request.FILES.get('thumb', False)
        sku = serial_number_generator(10).upper()

        if not upc:
            upc = serial_number_generator(12).upper()
        if not quantity:
            quantity = selected_product.quantity
        if not buy_price:
            buy_price = selected_product.buy_price
        if not sell_price:
            sell_price = selected_product.sell_price
        if not discount_price:
            discount_price = selected_product.discount_price

        new_thumbnail_size = Size(en_title=en_title,
                                  fr_title=fr_title,
                                  ar_title=ar_title,
                                  upc=upc,
                                  sku=sku,
                                  quantity=int(quantity),
                                  buy_price=int(buy_price),
                                  sell_price=int(sell_price),
                                  discount_price=int(discount_price),
                                  show_thumb=True,
                                  thumb=thumb,
                                  )
        new_thumbnail_size.save()
        selected_product.size.add(new_thumbnail_size)

        quantity = 0
        for selected_product_size in selected_product.size.all():
            quantity += selected_product_size.quantity
        selected_product.quantity = quantity
        selected_product.save()

    return {
        'url': url,
    }


def edit_thumbnail_size(request, sku, index):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_size = Size.objects.all().get(id=index)
    if request.method == 'POST':
        en_title = request.POST.get('en_title', False)
        fr_title = request.POST.get('fr_title', False)
        ar_title = request.POST.get('ar_title', False)
        quantity = request.POST.get('quantity', False)
        buy_price = request.POST.get('buy_price', False)
        sell_price = request.POST.get('sell_price', False)
        discount_price = request.POST.get('discount_price', False)
        thumb = request.FILES.get('thumb', False)

        if en_title:
            selected_size.en_title = en_title
        if fr_title:
            selected_size.fr_title = fr_title
        if ar_title:
            selected_size.ar_title = ar_title
        if quantity:
            selected_size.quantity = quantity
        if buy_price:
            selected_size.buy_price = buy_price
        if sell_price:
            selected_size.sell_price = sell_price
        if discount_price:
            selected_size.discount_price = discount_price
        if thumb:
            selected_size.thumb = thumb

        selected_size.save()

        quantity = 0
        for selected_product_size in selected_product.size.all():
            quantity += selected_product_size.quantity
        selected_product.quantity = quantity
        selected_product.save()

    return {
        'url': url,
    }


def delete_size(sku, index):
    url = "/shop-manager/inventory-edit.html"
    selected_product = Product.objects.all().get(sku=sku)
    selected_size = Size.objects.all().get(id=index)
    selected_size.delete()

    quantity = 0
    for selected_product_size in selected_product.size.all():
        quantity += selected_product_size.quantity
    selected_product.quantity = quantity
    selected_product.save()

    return {
        'url': url,
    }


def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
