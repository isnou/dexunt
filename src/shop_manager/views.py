from django.shortcuts import render, redirect
from . import inventory_actions, e_shop_actions, clips_actions
from .models import Product, Size, Feature, ShowcaseProduct
from main_shop.models import IntroThumb, IntroBanner ,Showcase


def manager_dashboard(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/shop-manager/dashboard.html"
    for product in ShowcaseProduct.objects.all():
        product.delete()
    for thumb in IntroThumb.objects.all():
        thumb.delete()
    for banner in IntroBanner.objects.all():
        banner.delete()

    context = {
    }
    return render(request, url, context)


def inventory(request, action, sku):
    try:
        inventory_products_list = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No products")
    try:
        e_shop_products_list = ShowcaseProduct.objects.all()
    except ShowcaseProduct.DoesNotExist:
        raise Http404("No products")

    inventory_products = inventory_products_list.order_by('en_title')
    e_shop_products = e_shop_products_list.order_by('en_title')

    direction = request.session.get('language')
    url = direction + "/shop-manager/inventory.html"
    tab = 'main'

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
    if action == "refresh_e_shop_product":
        url = direction + inventory_actions.refresh_e_shop_product().get('url')
        tab = 'e_shop'
    if action == "delete_e_shop_product":
        ShowcaseProduct.objects.all().get(sku=sku).delete()
        tab = 'e_shop'
    if action == "publish_e_shop_product":
        url = direction + inventory_actions.publish_e_shop_product(sku).get('url')
        tab = 'e_shop'
    if action == "unpublish_e_shop_product":
        url = direction + inventory_actions.unpublish_e_shop_product(sku).get('url')
        tab = 'e_shop'

    context = {
        'inventory_products': inventory_products,
        'e_shop_products': e_shop_products,
        'tab':tab,
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
        url = direction + inventory_actions.edit_size(request, sku, index).get('url')
    if action == "add_thumbnail_size":
        url = direction + inventory_actions.add_thumbnail_size(request, sku).get('url')
    if action == "edit_thumbnail_size":
        url = direction + inventory_actions.edit_thumbnail_size(request, sku, index).get('url')
    if action == 'delete_size':
        url = direction + inventory_actions.delete_size(sku, index).get('url')
    if action == 'delete_feature':
        Feature.objects.all().get(id=index).delete()
    if action == "edit_e_shop_product":
        url = direction + inventory_actions.edit_e_shop_product(request, sku).get('url')

    selected_product = Product.objects.all().get(sku=sku)
    sizes = selected_product.size.all().exclude(show_thumb=True)
    thumbnail_sizes = selected_product.size.all().exclude(show_thumb=False)

    context = {
        'selected_product': selected_product,
        'sizes': sizes,
        'thumbnail_sizes': thumbnail_sizes,
    }
    return render(request, url, context)

def inventory_preparation(request, action, sku):
    direction = request.session.get('language')
    url = direction + "/shop-manager/inventory-preparation.html"

    if action == "edit_e_shop_product":
        url = direction + inventory_actions.edit_e_shop_product(request, sku).get('url')
    if action == "edit_e_shop_product_thumb":
        url = direction + inventory_actions.edit_e_shop_product_thumb(request, sku).get('url')
    if action == "prepare_product":
        url = direction + inventory_actions.prepare_product(request, sku).get('url')

    selected_product = ShowcaseProduct.objects.all().get(sku=sku)

    context = {
        'selected_product': selected_product,
    }
    return render(request, url, context)


def e_shop(request, action, detail, index):
    direction = request.session.get('language')
    url = direction + "/shop-manager/e-shop.html"
    intro_banners = e_shop_actions.initialisation().get('intro_banners').order_by('rank')
    intro_thumbs = e_shop_actions.initialisation().get('intro_thumbs').order_by('rank')

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
        'intro_banners': intro_banners,
        'intro_thumbs':intro_thumbs,
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
