from django.shortcuts import render, redirect
from . import inventory_actions, e_shop_actions, clips_actions
from .models import Product, Size, Feature, ShowcaseProduct
from main_shop.models import Intro ,Showcase ,RootDirectory ,SubDirectory ,Category


def manager_dashboard(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/shop-manager/dashboard.html"

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
    if action == "remove_product":
        ShowcaseProduct.objects.all().get(sku=sku).delete()
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
    tab = 'edit_product'

    # -----------------------------edit product
    if action == "edit_product":
        url = direction + inventory_actions.edit_product(request, sku).get('url')

    # -----------------------------edit photos
    if action == "add_new_photo":
        url = direction + inventory_actions.add_new_photo(request, sku).get('url')
        tab = 'edit_photo'
    if action == "delete_photo":
        Product.objects.all().get(sku=sku).album.all().get(id=index).delete()
        tab = 'edit_photo'

    # -----------------------------edit features
    if action == 'add_new_feature':
        url = direction + inventory_actions.add_new_feature(request, sku).get('url')
        tab = 'edit_feature'
    if action == 'edit_feature':
        url = direction + inventory_actions.edit_feature(request, index).get('url')
        tab = 'edit_feature'
    if action == 'delete_feature':
        Feature.objects.all().get(id=index).delete()
        tab = 'edit_feature'

    # -----------------------------edit sizes
    if action == "add_new_size":
        url = direction + inventory_actions.add_new_size(request, sku).get('url')
        tab = 'edit_size'
    if action == "edit_size":
        url = direction + inventory_actions.edit_size(request, sku, index).get('url')
        tab = 'edit_size'

    # -----------------------------edit thumb sizes
    if action == "add_thumbnail_size":
        url = direction + inventory_actions.add_thumbnail_size(request, sku).get('url')
    if action == "edit_thumbnail_size":
        url = direction + inventory_actions.edit_thumbnail_size(request, sku, index).get('url')
    if action == 'delete_size':
        url = direction + inventory_actions.delete_size(sku, index).get('url')

    selected_product = Product.objects.all().get(sku=sku)
    sizes = selected_product.size.all().exclude(show_thumb=True)
    thumbnail_sizes = selected_product.size.all().exclude(show_thumb=False)

    context = {
        'selected_product': selected_product,
        'sizes': sizes,
        'thumbnail_sizes': thumbnail_sizes,
        'tab': tab,
    }
    return render(request, url, context)


def inventory_preparation(request, action, sku):
    direction = request.session.get('language')
    url = direction + "/shop-manager/inventory-preparation.html"

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

    if not Intro.objects.all().filter(id=1).exists():
        Intro(id=1,).save()
    intro = Intro.objects.all().get(id=1)
    try:
        all_products = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No products")

    tab = 'ad_showcase'

    # -----------------------------intro
    if action == "edit_intro":
        url = direction + e_shop_actions.edit_intro(request).get('url')
        tab = 'main_page'
    if action == "fix_intro":
        intro.fixed = True
        intro.save()
        tab = 'main_page'
    if action == "unfix_intro":
        intro.fixed = False
        intro.save()
        tab = 'main_page'
    if action == "stretch_intro":
        intro.repeat = True
        intro.save()
        tab = 'main_page'
    if action == "repeat_intro":
        intro.repeat = False
        intro.save()
        tab = 'main_page'

    # -----------------------------ad & showcase
    if action == "edit_single_flash":
        url = direction + e_shop_actions.edit_single_flash(request, detail).get('url')
    if action == "edit_multiple_flash":
        url = direction + e_shop_actions.edit_multiple_flash(request, detail).get('url')
    if action == "edit_grid_showcase":
        url = direction + e_shop_actions.edit_grid_showcase(request, detail).get('url')
    if action == "edit_slider_showcase":
        url = direction + e_shop_actions.edit_slider_showcase(request, detail).get('url')
    if action == "edit_small_ad":
        url = direction + e_shop_actions.edit_small_ad(request, detail).get('url')
    if action == "edit_big_ad":
        url = direction + e_shop_actions.edit_big_ad(request, detail).get('url')
    if action == "delete_showcase":
        Showcase.objects.all().get(sku=detail).delete()
    if action == "up_showcase":
        url = direction + e_shop_actions.up_showcase(detail, index).get('url')
    if action == "down_showcase":
        url = direction + e_shop_actions.down_showcase(detail, index).get('url')
    if action == "activate":
        showcase = Showcase.objects.all().get(sku=detail)
        showcase.publish = True
        showcase.save()
    if action == "deactivate":
        showcase = Showcase.objects.all().get(sku=detail)
        showcase.publish = False
        showcase.save()
    if action == "add_product_to_showcase":
        url = direction + e_shop_actions.add_product_to_showcase(detail, index).get('url')
    if action == "remove_product_from_showcase":
        url = direction + e_shop_actions.remove_product_from_showcase(detail, index).get('url')

    # -----------------------------category
    if action == "edit_root":
        url = direction + e_shop_actions.edit_root(request, detail).get('url')
        tab = 'category'
    if action == "edit_directory":
        url = direction + e_shop_actions.edit_directory(request, detail).get('url')
        tab = 'category'


    if action == "edit_category":
        url = direction + e_shop_actions.edit_category(request, detail).get('url')
        tab = 'category'
    if action == "activate_category":
        category = Category.objects.all().get(sku=detail)
        category.publish = True
        category.save()
        tab = 'category'
    if action == "deactivate_category":
        category = Category.objects.all().get(sku=detail)
        category.publish = False
        category.save()
        tab = 'category'
    if action == "delete_category":
        Category.objects.all().get(sku=detail).delete()
        tab = 'category'
    if action == "up_category":
        url = direction + e_shop_actions.up_category(detail, index).get('url')
        tab = 'category'
    if action == "down_category":
        url = direction + e_shop_actions.down_category(detail, index).get('url')
        tab = 'category'
    if action == "add_product_to_category":
        url = direction + e_shop_actions.add_product_to_category(detail, index).get('url')
        tab = 'category'
    if action == "remove_product_from_category":
        url = direction + e_shop_actions.remove_product_from_category(detail, index).get('url')
        tab = 'category'

    context = {
        'all_products': all_products,
        'tab':tab,
    }
    return render(request, url, context)
