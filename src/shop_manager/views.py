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
    if action == "add_new_photo":
        url = direction + inventory_actions.add_new_photo(request, sku).get('url')
    if action == "add_new_size":
        url = direction + inventory_actions.add_new_size(request, sku).get('url')
    if action == "delete_product":
        Product.objects.all().get(sku=sku).delete()

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory_product(request, action, sku, identity):
    lang = request.session.get('language')
    direction = request.session.get('direction')
    url = direction + "shop-manager/inventory-product.html"
    if action == 'add_en_features':
        url = direction + inventory_actions.add_features(request, 'english', sku).get('url')
    if action == 'add_fr_features':
        url = direction + inventory_actions.add_features(request, 'french', sku).get('url')
    if action == 'add_ar_features':
        url = direction + inventory_actions.add_features(request, 'arabic', sku).get('url')
    if action == 'delete_feature':
        Product.objects.all().get(sku=sku).features.all().get(id=identity).delete()

    selected_product = Product.objects.all().get(sku=sku)
    photos = Product.objects.all().filter(en_product_title=selected_product.en_product_title).filter(type='photo')
    features = selected_product.features.all()
    english_features = features.filter(language='english').order_by('type')
    french_features = features.filter(language='french').order_by('type')
    arabic_features = features.filter(language='arabic').order_by('type')
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
