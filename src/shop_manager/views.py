from django.shortcuts import render, redirect
from . import inventory_actions, e_shop_actions, clips_actions
from .models import Product
from main_shop.models import Layout


def manager_dashboard(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/shop-manager/dashboard.html"

    context = {
    }
    return render(request, url, context)


def inventory(request, action, sku):
    direction = request.session.get('language')
    url = direction + "/shop-manager/inventory.html"

    if action == "add_new_product":
        url = direction + inventory_actions.add_new_product(request).get('url')
    if action == "add_new_variant":
        url = direction + inventory_actions.add_new_variant(request, sku).get('url')
    if action == "add_quantity":
        url = direction + inventory_actions.add_quantity(sku).get('url')
    if action == "remove_quantity":
        url = direction + inventory_actions.remove_quantity(sku).get('url')
    if action == "publish":
        url = direction + inventory_actions.publish(sku).get('url')
    if action == "unpublish":
        url = direction + inventory_actions.unpublish(sku).get('url')
    if action == "delete_product":
        Product.objects.all().get(sku=sku).delete()

    context = {
    }
    return render(request, url, context)


def inventory_edit(request, action, sku, index):
    direction = request.session.get('language')
    url = direction + "/shop-manager/inventory-edit.html"

    if action == "edit_product":
        url = direction + inventory_actions.edit_product(request, sku).get('url')
    if action == "add_new_photo":
        url = direction + inventory_actions.add_new_photo(request, sku).get('url')
    if action == "delete_photo":
        Product.objects.all().get(sku=sku).album.all().get(id=index).delete()
    if action == 'add_new_feature':
        url = direction + inventory_actions.add_new_feature(request, sku).get('url')
    if action == 'edit_feature':
        url = direction + inventory_actions.edit_feature(request, index).get('url')
    if action == "add_new_size":
        url = direction + inventory_actions.add_new_size(request, sku).get('url')
    if action == "edit_size":
        url = direction + inventory_actions.edit_size(request, sku).get('url')
        sku = inventory_actions.edit_size(request, sku).get('sku')
    if action == "add_a_set":
        url = direction + inventory_actions.add_a_set(request, sku).get('url')
    if action == "edit_a_set":
        url = direction + inventory_actions.edit_a_set(request, sku).get('url')
        sku = inventory_actions.edit_a_set(request, sku).get('sku')
    if action == 'delete_attached':
        url = direction + inventory_actions.delete_attached(sku, index).get('url')
        sku = inventory_actions.delete_attached(sku, index).get('sku')
    if action == 'delete_feature':
        Product.objects.all().get(sku=sku).features.all().get(id=index).delete()

    selected_product = Product.objects.all().get(sku=sku)
    attached_products = Collection.objects.all().get(attach=selected_product.attach)
    sizes = Product.objects.all().filter(type='size')
    sets = Product.objects.all().filter(type='set')

    context = {
        'sets': sets,
        'sizes': sizes,
        'selected_product': selected_product,
    }
    return render(request, url, context)


def e_shop(request, action, detail, index):
    direction = request.session.get('language')
    url = direction + "/shop-manager/e-shop.html"

    if action == "edit_main_banner":
        url = direction + e_shop_actions.main_banner(request, detail).get('url')
    if action == "edit_thumb_banner":
        url = direction + e_shop_actions.thumb_banner(request, detail).get('url')
    if action == "add_movable_banner":
        url = direction + e_shop_actions.add_movable_banner(request).get('url')
    if action == "add_showcase":
        url = direction + e_shop_actions.add_showcase(request).get('url')
    if action == "delete":
        url = direction + e_shop_actions.delete(index).get('url')
    if action == "up":
        url = direction + e_shop_actions.up(index).get('url')
    if action == "down":
        url = direction + e_shop_actions.down(index).get('url')
    if action == "refresh_points":
        url = direction + clips_actions.points(request).get('url')
    if action == "refresh_delivery":
        url = direction + clips_actions.delivery(request).get('url')
    if action == "refresh_solidarity":
        url = direction + clips_actions.solidarity(request).get('url')
    if action == "points_to_product":
        url = direction + clips_actions.points_to_product(request, index).get('url')
    if action == "value_to_product":
        url = direction + clips_actions.value_to_product(request, index).get('url')

    context = {
    }
    return render(request, url, context)


def e_shop_edit(request, action, detail, index):
    direction = request.session.get('language')
    url = direction + "/shop-manager/e-shop-edit.html"

    if action == "showcase":
        url = direction + e_shop_actions.showcase(request, index).get('url')
    if action == "banner":
        url = direction + e_shop_actions.banner(request, index).get('url')
    if action == "link_product":
        url = direction + e_shop_actions.link(detail, index).get('url')
        detail = 'showcase'
    if action == "unlink_product":
        url = direction + e_shop_actions.unlink(detail, index).get('url')
        detail = 'showcase'

    selected_layout = Layout.objects.all().get(id=index)
    selected_layout_type = detail

    context = {
        'selected_layout': selected_layout,
        'selected_layout_type': selected_layout_type,
    }
    return render(request, url, context)
