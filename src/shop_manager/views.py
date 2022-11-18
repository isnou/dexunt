from django.shortcuts import render, redirect
from . import actions
from . import inventory_actions
from .models import InventoryProduct


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
        url = direction + inventory_actions.add_new_product(request, lang).get('url')
    if action == "delete_product":
        url = direction + inventory_actions.delete_product(request, lang, sku).get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory_product(request, action, sku, identity):
    lang = request.session.get('language')
    direction = request.session.get('direction')
    url = direction + "shop-manager/inventory-product.html"
    if action == 'edit':
        url = direction + inventory_actions.edit(request, lang, sku).get('url')
    if action == 'add_photo':
        url = direction + inventory_actions.add_new_photo(request, lang, sku).get('url')
    if action == 'delete_photo':
        selected_product = InventoryProduct.objects.all()
        selected_photos = selected_product.album.all()
        selected_photos.get(id=identity).delete()
    if action == 'add_en_features':
        url = direction + inventory_actions.add_features(request, 'english', sku).get('url')
    if action == 'add_fr_features':
        url = direction + inventory_actions.add_features(request, 'french', sku).get('url')
    if action == 'add_ar_features':
        url = direction + inventory_actions.add_features(request, 'arabic', sku).get('url')

    all_products = InventoryProduct.objects.all()
    selected_product = all_products.get(sku=sku)
    features = selected_product.features.all()
    english_features = features.filter(language='english').order_by('type')
    french_features = features.filter(language='french').order_by('type')
    arabic_features = features.filter(language='arabic').order_by('type')
    photos = selected_product.album.all()
    features_count = features.count()
    photos_count = photos.count()

    context = {
        'lang': lang,
        'english_features': english_features,
        'french_features': french_features,
        'arabic_features': arabic_features,
        'photos': photos,
        'features_count': features_count,
        'photos_count': photos_count,
        'selected_product': selected_product,
    }
    return render(request, url, context)
