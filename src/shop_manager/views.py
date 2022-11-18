from django.shortcuts import render, redirect
from . import actions
from . import inventory_actions
from .models import InventoryProduct


def manager_dashboard(request, action):
    lang = "en"
    url = "ltr/shop-manager/dashboard.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory(request, action, sku):
    lang = "en"
    url = "ltr/shop-manager/inventory.html"
    if action == "add_new_product":
        url = inventory_actions.add_new_product(request, lang).get('url')
    if action == "delete_product":
        url = inventory_actions.delete_product(request, lang, sku).get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory_product(request, action, sku, identity):
    lang = "en"
    url = "ltr/shop-manager/inventory-product.html"
    if action == 'edit':
        url = inventory_actions.edit(request, lang, sku).get('url')
    if action == 'add_photo':
        url = inventory_actions.add_new_photo(request, lang, sku).get('url')

    all_products = InventoryProduct.objects.all()
    selected_product = all_products.get(sku=sku)
    features = selected_product.features.all()
    photos = selected_product.album.all()
    features_count = features.count()
    photos_count = photos.count()

    context = {
        'lang': lang,
        'features': features,
        'photos': photos,
        'features_count': features_count,
        'photos_count': photos_count,
        'selected_product': selected_product,
    }
    return render(request, url, context)


def add_product(request, action):
    result = actions.add_new_product(request, action)
    lang = result.get('lang')
    url = result.get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def view_product(request, action, sku):
    result = actions.view(request, action, sku)
    lang = result.get('lang')
    url = result.get('url')
    product_to_view = result.get('product_to_view')
    features = result.get('features')
    photos = result.get('photos')
    features_count = features.count()
    photos_count = photos.count()

    context = {
        'lang': lang,
        'product_to_view': product_to_view,
        'features': features,
        'photos': photos,
        'features_count': features_count,
        'photos_count': photos_count,
    }
    return render(request, url, context)


def edit_product(request, action, sku):
    result = actions.edit(request, action, sku)
    lang = result.get('lang')
    url = result.get('url')
    product_to_edit = result.get('product_to_edit')

    context = {
        'lang': lang,
        'product_to_edit': product_to_edit,
    }
    return render(request, url, context)


def delete_product(request, action, sku):
    result = actions.delete(request, action, sku)
    lang = result.get('lang')
    url = result.get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def delete_option(request, action, sku, ident):
    result = actions.option_delete(request, action, sku, ident)
    lang = result.get('lang')
    url = result.get('url')
    product_to_view = result.get('product_to_view')
    features = result.get('features')
    photos = result.get('photos')
    features_count = features.count()
    photos_count = photos.count()

    context = {
        'lang': lang,
        'product_to_view': product_to_view,
        'features': features,
        'photos': photos,
        'features_count': features_count,
        'photos_count': photos_count,
    }
    return render(request, url, context)
