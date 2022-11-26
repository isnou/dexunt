from django.shortcuts import render, redirect
from . import inventory_actions
from .models import Product


def manager_dashboard(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
        request.session['direction'] = 'ltr/'
    lang = request.session.get('language')
    direction = request.session.get('direction')
    url = direction + "shop-manager/dashboard.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory(request, action, sku):
    lang = request.session.get('language')
    direction = request.session.get('direction')
    url = direction + "shop-manager/inventory.html"
    if action == "add_new_product":
        url = direction + inventory_actions.add_new_product(request).get('url')
    if action == "delete_product":
        selected_product = Product.objects.all().get(sku=sku)
        if selected_product.type == 'main':
            Product.objects.all().filter(en_product_title=selected_product.en_product_title).delete()
        else:
            selected_product.delete()
    if action == "add_quantity":
        url = direction + inventory_actions.add_quantity(request, sku).get('url')
    if action == "remove_quantity":
        url = direction + inventory_actions.remove_quantity(request, sku).get('url')
    if action == "add_new_variant":
        url = direction + inventory_actions.add_new_variant(request, sku).get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory_product(request, action, sku, identity):
    lang = request.session.get('language')
    direction = request.session.get('direction')
    url = direction + "shop-manager/inventory-product.html"
    if action == "add_new_size":
        url = direction + inventory_actions.add_new_size(request, sku).get('url')
    if action == "add_new_photo":
        url = direction + inventory_actions.add_new_photo(request, sku).get('url')
    if action == "edit_photo":
        url = direction + inventory_actions.edit_photo(request, sku).get('url')
    if action == "add_a_set":
        url = direction + inventory_actions.add_a_set(request, sku).get('url')
    if action == "add_a_variant":
        url = direction + inventory_actions.add_a_variant(request, sku).get('url')
    if action == "edit_product":
        url = direction + inventory_actions.edit(request, sku).get('url')
    if action == "edit_a_set":
        url = direction + inventory_actions.edit_a_set(request, sku).get('url')
    if action == 'delete_variant':
        Product.objects.all().get(sku=sku).delete()
    if action == 'add_new_feature':
        url = direction + inventory_actions.add_new_feature(request, sku).get('url')
    if action == 'edit_feature':
        url = direction + inventory_actions.edit_feature(request, identity).get('url')
    if action == 'delete_feature':
        Product.objects.all().get(sku=sku).features.all().get(id=identity).delete()

    selected_product = Product.objects.all().get(sku=sku)
    variants = Product.objects.all().filter(en_product_title=selected_product.en_product_title).filter(type='variant')
    sets = Product.objects.all().filter(en_product_title=selected_product.en_product_title).filter(type='set')
    photos = Product.objects.all().filter(en_product_title=selected_product.en_product_title) \
        .filter(en_variant=selected_product.en_variant + ' photo').filter(type='photo')
    sizes = Product.objects.all().filter(en_product_title=selected_product.en_product_title) \
        .filter(en_variant=selected_product.en_variant + ' size').filter(type='size')
    features = selected_product.features.all()
    features_count = features.count()
    photos_count = photos.count()
    sizes_count = sizes.count()
    if sizes_count == 0:
        selected_product.type = 'main'
    else:
        selected_product.type = 'proto'
    variants_count = variants.count()
    if variants_count == 0:
        selected_product.type = 'main'
    else:
        selected_product.type = 'proto'
    sets_count = sets.count()
    if sets_count == 0:
        selected_product.type = 'main'
    else:
        selected_product.type = 'proto'

    context = {
        'lang': lang,

        'variants': variants,
        'variants_count': variants_count,

        'photos': photos,
        'photos_count': photos_count,

        'sets': sets,

        'sizes': sizes,
        'sizes_count': sizes_count,

        'features': features,
        'features_count': features_count,

        'selected_product': selected_product,
    }
    return render(request, url, context)
