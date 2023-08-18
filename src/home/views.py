from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from .models import Cart, SelectedProduct, get_cart, get_order
from .models import Coupon, apply_coupon
from .models import Province, Municipality
from management.models import Product, Variant, Option, Feature, Album, FlashProduct, Store
from management.forms import ProductForm, VariantForm, FeatureForm, OptionForm
from authentication.models import User


def home_page(request):
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
    direction = request.session.get('language')

    url = direction + "/home/main.html"

    if request.session.get('error_messages'):
        errors = request.session.get('error_messages')
        request.session['error_messages'] = None
    else:
        errors = None

    login_form = LoginForm()
    signup_form = SignupForm()

    all_stores = Store.objects.all().filter(is_activated=True).order_by('?')[:6]
    all_products = Variant.objects.all().filter(is_activated=True)[:15]
    all_flash_products = FlashProduct.objects.all().exclude(is_activated=False).order_by('?')[:10]

    for p in all_products:
        p.clean()

    for f in all_flash_products:
        f.clean()

    published_products = all_products[:10]
    published_flash_products = all_flash_products[:4]

    context = {
        'source_page': 'home-page',
        'errors': errors,
        'login_form': login_form,
        'signup_form': signup_form,
        'selected_cart': selected_cart,
        'published_products': published_products,
        'published_flash_products': published_flash_products,
        'all_stores': all_stores,
    }
    return render(request, url, context)

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')

def product_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')

    if action == 'regular_product':
        url = direction + "/home/regular/single-product.html"

        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            option_id = request.POST.get('option_id', False)
        else:
            variant_id = request.GET.get('variant_id')
            option_id = request.GET.get('option_id')

        selected_variant = Variant.objects.all().get(id=variant_id)

        if option_id:
            selected_option = Option.objects.all().get(id=option_id)
        else:
            selected_option = None

        context = {
            'source_page': 'product-page',
            'selected_option': selected_option,
            'selected_variant': selected_variant,
        }
        return render(request, url, context)

def shopping_cart_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
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
    direction = request.session.get('language')
    selected_order = get_order(request)

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
        if not request.user.is_authenticated:
            return render(request, direction + '/home/regular/guest/partials/municipalities.html', sub_context)
        else:
            return render(request, direction + '/home/regular/member/partials/municipalities.html', sub_context)
    if action == 'load_prices':
        if not request.user.is_authenticated:
            municipality_id = request.GET.get('municipality_id')
            municipality = Municipality.objects.all().get(id=municipality_id)

            selected_order.municipality = municipality
            selected_order.save()
            sub_context = {
                'selected_order': selected_order,
            }
            return render(request, direction + '/home/regular/guest/partials/prices.html', sub_context)
        else:
            address_id = request.GET.get('address_id')
            delivery_address = request.user.delivery_addresses.all().get(id=address_id)
            selected_order.delivery_type = delivery_address.delivery_type
            selected_order.municipality = delivery_address.municipality
            selected_order.save()

            sub_context = {
                'selected_order': selected_order,
            }
            return render(request, direction + '/home/regular/member/partials/prices.html', sub_context)
    if action == 'create_new_address':
        if request.method == 'POST':
            source_page = request.POST.get('source_page', False)
            municipality_id = request.POST.get('municipality_id', False)
            municipality = Municipality.objects.all().get(id=municipality_id)
            request.user.new_address(request, municipality)
            if source_page == 'order-page':
                return redirect('order-page', 'main')
            if source_page == 'customer-address':
                return redirect('customer-address', 'main')
    if action == 'load_summary':
        if not request.user.is_authenticated:
            delivery_type = request.GET.get('delivery_type')
            selected_order.delivery_type = delivery_type
            selected_order.save()

            sub_context = {
                'selected_order': selected_order,
            }
            return render(request, direction + '/home/regular/guest/partials/total-summary.html', sub_context)
        else:
            delivery_type = request.GET.get('delivery_type')
            selected_order.delivery_type = delivery_type
            selected_order.save()

            sub_context = {
                'selected_order': selected_order,
            }
            return render(request, direction + '/home/regular/member/partials/total-summary.html', sub_context)
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
