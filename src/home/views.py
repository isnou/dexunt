from django.shortcuts import render, redirect
from add_ons.functions import serial_number_generator
from add_ons.variables import get_cart, categories
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from .models import Cart, SelectedProduct
from .models import Coupon, apply_coupon
from .models import Province, Municipality
from management.models import Product, Variant, Option, Feature, Album, FlashProduct, Store, Category, Collection
from management.forms import ProductForm, VariantForm, FeatureForm, OptionForm
from authentication.models import User
from authentication.models import reset_users


def home_page(request):
    reset_users()
    selected_cart = get_cart(request)

    if request.user.is_authenticated:
        if request.user.is_provider:
            return redirect('provider-sales', 'main')
        if request.user.is_cash_manager:
            return redirect('cash-wallet', 'main')
        if request.user.is_member:
            return redirect('member-orders', 'main')

    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    if not request.session.get('direction', None):
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')

    request.session['variant_id'] = None
    request.session['option_id'] = None
    request.session['collection_id'] = None

    url = direction + "/home/main.html"

    if request.session.get('error_messages'):
        errors = request.session.get('error_messages')
        request.session['error_messages'] = None
    else:
        errors = None

    login_form = LoginForm()
    signup_form = SignupForm()

    all_stores = Store.objects.all().filter(is_activated=True).order_by('?')[:6]
    all_products = Product.objects.all().filter(is_activated=True)
    all_flash_products = FlashProduct.objects.all().exclude(is_activated=False).order_by('?')[:10]
    categories = Category.objects.all().filter(is_activated=True).order_by('rates')


    grid_products = all_products
    published_flash_products = all_flash_products[:4]

    context = {
        'source_page': 'home-page',
        'errors': errors,
        'login_form': login_form,
        'signup_form': signup_form,
        'selected_cart': selected_cart,
        'grid_products': grid_products,
        'published_flash_products': published_flash_products,
        'all_stores': all_stores,
        'categories': categories,
    }
    return render(request, url, context)

def shop_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')

    if action == 'collection':
        url = direction + "/home/grid.html"
        if request.GET.get('collection_id', False):
            collection_id = request.GET.get('collection_id')
            request.session['collection_id'] = collection_id
        else:
            collection_id = request.session.get('collection_id')

        selected_collection = Collection.objects.all().get(id=collection_id)

        login_form = LoginForm()
        signup_form = SignupForm()

        categories = Category.objects.all().filter(is_activated=True).order_by('rates')

        context = {
            'selected_collection': selected_collection,
            'source_page': 'grid-shop-page',
            'login_form': login_form,
            'signup_form': signup_form,
            'categories': categories,
        }
        return render(request, url, context)

    if action == 'category':
        url = direction + "/home/grid.html"
        if request.GET.get('category_id', False):
            category_id = request.GET.get('category_id')
            request.session['category_id'] = category_id
        else:
            category_id = request.session.get('category_id')

        selected_collection = Category.objects.all().get(id=category_id)

        login_form = LoginForm()
        signup_form = SignupForm()

        categories = Category.objects.all().filter(is_activated=True).order_by('rates')

        context = {
            'selected_collection': selected_collection,
            'source_page': 'grid-shop-page',
            'login_form': login_form,
            'signup_form': signup_form,
            'categories': categories,
        }
        return render(request, url, context)

    if action == 'store':
        url = direction + "/home/store.html"
        if request.GET.get('store_id', False):
            store_id = request.GET.get('store_id')
            request.session['store_id'] = store_id
        else:
            store_id = request.session.get('store_id')

        selected_store = Store.objects.all().get(id=store_id)

        login_form = LoginForm()
        signup_form = SignupForm()

        categories = Category.objects.all().filter(is_activated=True).order_by('rates')

        context = {
            'selected_store': selected_store,
            'source_page': 'grid-shop-page',
            'login_form': login_form,
            'signup_form': signup_form,
            'categories': categories,
        }
        return render(request, url, context)

def product_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')

    if action == 'regular_product':
        url = direction + "/home/regular/single-product.html"

        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', None)
            option_id = request.POST.get('option_id', None)
        else:
            variant_id = request.GET.get('variant_id', None)
            option_id = request.GET.get('option_id', None)

        if not variant_id:
            variant_id = request.session.get('variant_id')
            option_id = request.session.get('option_id')

        selected_variant = Variant.objects.all().get(id=variant_id)

        if option_id:
            selected_option = Option.objects.all().get(id=option_id)
        else:
            if selected_variant.selected_option():
                selected_option = selected_variant.selected_option()
            else:
                selected_option = selected_variant.admin_selected_option()

        request.session['variant_id'] = selected_variant.id
        request.session['option_id'] = selected_option.id

        context = {
            'source_page': 'product-page',
            'selected_option': selected_option,
            'selected_variant': selected_variant,
        }
        return render(request, url, context)

def shopping_cart_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    selected_cart = get_cart(request)

    coupon_message = request.session.get('coupon_message')
    request.session['coupon_message'] = None

    if action == 'main':
        url = direction + "/home/regular/shopping-cart.html"

        if selected_cart.selected_products.all().count():
            context = {
                'source_page': 'shopping-cart',
                'selected_cart': selected_cart,
                'coupon_message': coupon_message,
            }
            return render(request, url, context)
        else:
            return redirect('home-page')
    if action == 'add_regular_product':
        selected_option = Option.objects.all().get(id=request.GET.get('option_id'))
        selected_cart.add_product(selected_option)
        return redirect('shopping-cart', 'main')
    if action == 'apply_coupon':
        if request.method == 'POST':
            apply_coupon(request, selected_cart)
            return redirect('shopping-cart', 'main')
    if action == 'add_quantity':
        selected_product = SelectedProduct.objects.all().get(id=request.GET.get('product_id'))
        if selected_product.option.quantity > selected_product.quantity:
            if selected_product.option.max_quantity > selected_product.quantity:
                selected_product.quantity += 1
                selected_product.save()
        return redirect('shopping-cart', 'main')
    if action == 'remove_quantity':
        selected_product = SelectedProduct.objects.all().get(id=request.GET.get('product_id'))
        if selected_product.quantity > 1:
            selected_product.quantity -= 1
            selected_product.save()
        else:
            selected_product.delete()
        if selected_cart.selected_products.all().count():
            return redirect('shopping-cart', 'main')
        else:
            return redirect('home-page')
    if action == 'remove_product':
        selected_product = SelectedProduct.objects.all().get(id=request.GET.get('product_id'))
        selected_product.delete()
        return redirect('home-page')

def order_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    selected_order = get_cart(request).get_order(request)

    request.session['coupon_message'] = None
    provinces = Province.objects.all()

    if action == 'main':
        if not request.user.is_authenticated:
            url = direction + "/home/regular/guest/order-page.html"
        else:
            url = direction + "/home/regular/member/order-page.html"

        context = {
            'source_page': 'order-page',
            'selected_order': selected_order,
            'provinces': provinces,
        }
        return render(request, url, context)
    if action == 'load_client_name':
        full_name = request.GET.get('full_name')
        selected_order.client_name = full_name
        selected_order.save()
    if action == 'load_client_phone':
        phone = request.GET.get('phone')
        selected_order.client_phone = phone
        selected_order.save()
    if action == 'load_municipalities':
        province_id = request.GET.get('province_id')
        province = Province.objects.all().get(id=province_id)

        sub_context = {
            'selected_order': selected_order,
            'province': province,
        }
        return render(request, direction + '/home/regular/partials/municipalities.html', sub_context)
    if action == 'load_prices':
        if not request.user.is_authenticated:
            municipality_id = request.GET.get('municipality_id')
            municipality = Municipality.objects.all().get(id=municipality_id)
            selected_order.municipality = municipality
            selected_order.save()
        else:
            address_id = request.GET.get('address_id')
            delivery_address = request.user.delivery_addresses.all().get(id=address_id)
            selected_order.municipality = delivery_address.municipality
            selected_order.save()
        sub_context = {
            'selected_order': selected_order,
        }
        return render(request, direction + '/home/regular/partials/prices.html', sub_context)
    if action == 'load_summary':
        if not request.user.is_authenticated:
            delivery_type = request.GET.get('delivery_type')
            selected_order.delivery_type = delivery_type
            selected_order.save()
        else:
            delivery_type = request.GET.get('delivery_type')
            selected_order.delivery_type = delivery_type
            selected_order.save()
        sub_context = {
            'selected_order': selected_order,
        }
        return render(request, direction + '/home/regular/partials/total-summary.html', sub_context)
    if action == 'place_order':
        selected_order.placing(request)

        if not request.user.is_authenticated:
            url = direction + "/home/regular/guest/checkout-review.html"
        else:
            url = direction + "/home/regular/member/checkout-review.html"

        context = {
            'selected_order': selected_order,
        }
        return render(request, url, context)

def order_tracking(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/home/order-tracking.html"

        if request.user.is_authenticated:
            order_ref = request.GET.get('order_ref')
            selected_order = request.user.all_orders.all().get(ref=order_ref)

        context = {
            'selected_order': selected_order,
        }
        return render(request, url, context)

def change_language(request):
    language = request.GET.get('language', False)
    source = request.GET.get('source_page', None)

    request.session['language'] = language
    if language == 'ar-dz':
        request.session['direction'] = 'rtl'
    if language == 'en-us' or language == 'fr-fr':
        request.session['direction'] = 'ltr'

    if source == 'home-page':
        return redirect('home-page')
    if source == 'product-page':
        return redirect('product-page', 'regular_product')
    if source == 'shopping-cart':
        return redirect('shopping-cart', 'main')
    if source == 'order-page':
        return redirect('order-page', 'main')
    if source == 'grid-shop-page':
        return redirect('shop-page', 'grid')





