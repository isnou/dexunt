from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from shop_manager.models import ShowcaseProduct, Product
from sell_manager.models import Cart, Province
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate

from .models import Showcase, Wished, Booked
from . import grid_shop_actions
from add_ons import functions


def main_shop_home(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"

    login_form = LoginForm()
    signup_form = SignupForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, url, context)


def change_language(request, language):
    if language == 'en':
        request.session['language'] = 'en'
    if language == 'fr':
        request.session['language'] = 'fr'
    if language == 'ar':
        request.session['language'] = 'ar'
    return redirect('main-shop-home')


def product(request, sku, size_sku):
    direction = request.session.get('language')
    url = direction + "/main-shop/product.html"

    if request.session.get('book_it_message', None):
        book_it_message = request.session.get('book_it_message')
        request.session['book_it_message'] = None
    else:
        book_it_message = None

    if request.session.get('wish_it_message', None):
        wish_it_message = request.session.get('wish_it_message')
        request.session['wish_it_message'] = None
    else:
        wish_it_message = None

    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    selected_product = Product.objects.all().get(sku=sku)

    if ShowcaseProduct.objects.all().filter(en_title=selected_product.en_title).exists():
        variant = ShowcaseProduct.objects.all().get(en_title=selected_product.en_title)
    else:
        variant = None

    if not size_sku == 'main':
        selected_size = selected_product.size.all().get(sku=size_sku)
    else:
        selected_size = None

    if cart.product.all().filter(product_sku=sku).exists():
        if cart.product.all().filter(size_sku=size_sku).exists():
            update = True
        elif size_sku == 'main':
            update = True
        else:
            update = False
    else:
        update=False

    buy_now = False
    if not cart.product.all().count():
        buy_now = True

    context = {
        'selected_product': selected_product,
        'selected_size': selected_size,
        'variant': variant,
        'size_sku': size_sku,
        'update': update,
        'buy_now': buy_now,
        'book_it_message': book_it_message,
        'wish_it_message': wish_it_message,
    }
    return render(request, url, context)


def grid_shop(request, action, ref):
    direction = request.session.get('language')
    url = direction + "/main-shop/grid-shop.html"

    products = None

    if action == 'all':
        url = direction + grid_shop_actions.all_products(request).get('url')
        products = grid_shop_actions.all_products(request).get('products_list')

    if action == 'best_sellers':
        url = direction + grid_shop_actions.best_sellers(request).get('url')
        products = grid_shop_actions.best_sellers(request).get('products_list')

    if action == 'new_arrivals':
        url = direction + grid_shop_actions.new_arrivals(request).get('url')
        products = grid_shop_actions.new_arrivals(request).get('products_list')

    if action == 'top_rated':
        url = direction + grid_shop_actions.top_rated(request).get('url')
        products = grid_shop_actions.top_rated(request).get('products_list')

    if action == 'showcase':
        url = direction + grid_shop_actions.showcase_products(request, ref).get('url')
        products = grid_shop_actions.showcase_products(request, ref).get('products_list')

    context = {
        'products': products,
    }
    return render(request, url, context)

def book_it(request, sku, size_sku):
    if request.user.is_authenticated:
        user = request.user
        selected_product = Product.objects.all().get(sku=sku)

        if not size_sku == 'main':
            selected_size = selected_product.size.all().get(sku=size_sku)
            if selected_size.show_thumb:
                product_to_book = Booked(thumb = selected_size.thumb,
                                         product_sku = selected_product.sku,
                                         size_sku = size_sku,
                                         en_name = selected_product.en_title,
                                         fr_name = selected_product.fr_title,
                                         ar_name = selected_product.ar_title,
                                         en_spec = selected_product.en_spec,
                                         fr_spec = selected_product.fr_spec,
                                         ar_spec = selected_product.ar_spec,
                                         en_detail = selected_size.en_title,
                                         fr_detail = selected_size.fr_title,
                                         ar_detail = selected_size.ar_title,
                                         )
                product_to_book.save()
            else:
                product_to_book = Booked(thumb = selected_product.album.all()[:1].get().image,
                                         product_sku = selected_product.sku,
                                         size_sku = size_sku,
                                         en_name = selected_product.en_title,
                                         fr_name = selected_product.fr_title,
                                         ar_name = selected_product.ar_title,
                                         en_spec = selected_product.en_spec,
                                         fr_spec = selected_product.fr_spec,
                                         ar_spec = selected_product.ar_spec,
                                         en_detail = selected_size.en_title,
                                         fr_detail = selected_size.fr_title,
                                         ar_detail = selected_size.ar_title,
                                         )
                product_to_book.save()
        else:
            product_to_book = Booked(thumb=selected_product.album.all()[:1].get().image,
                                     product_sku=selected_product.sku,
                                     size_sku=size_sku,
                                     en_name=selected_product.en_title,
                                     fr_name=selected_product.fr_title,
                                     ar_name=selected_product.ar_title,
                                     en_spec=selected_product.en_spec,
                                     fr_spec=selected_product.fr_spec,
                                     ar_spec=selected_product.ar_spec,
                                     )
            product_to_book.save()

        if user.booked.filter(product_sku=product_to_book.product_sku).exists():
            if size_sku == 'main':
                request.session['book_it_message'] = 'exists'
            else:
                if user.booked.filter(size_sku=size_sku).exists():
                    request.session['book_it_message'] = 'exists'
                else:
                    user.booked.add(product_to_book)
                    request.session['book_it_message'] = 'success'
        else:
            user.booked.add(product_to_book)
            request.session['book_it_message'] = 'success'

        return redirect('single-product' ,sku ,size_sku)

    else:
        return redirect ('login-page')

def un_book_it(request, sku, size_sku):
    if request.user.is_authenticated:
        user = request.user
        if size_sku == 'main':
            selected_product = user.booked.all().get(product_sku=sku)
            selected_product.delete()
        else:
            selected_product = user.booked.all().get(size_sku=size_sku)
            selected_product.delete()
        return redirect('booked-products-page')

def wish_it(request, sku, size_sku):
    if request.user.is_authenticated:
        user = request.user
        selected_product = Product.objects.all().get(sku=sku)

        if not size_sku == 'main':
            selected_size = selected_product.size.all().get(sku=size_sku)
            if selected_size.show_thumb:
                wished_product = Wished(thumb = selected_size.thumb,
                                         product_sku = selected_product.sku,
                                         size_sku = selected_size.sku,
                                         en_name = selected_product.en_title,
                                         fr_name = selected_product.fr_title,
                                         ar_name = selected_product.ar_title,
                                         en_spec = selected_product.en_spec,
                                         fr_spec = selected_product.fr_spec,
                                         ar_spec = selected_product.ar_spec,
                                         en_detail = selected_size.en_title,
                                         fr_detail = selected_size.fr_title,
                                         ar_detail = selected_size.ar_title,
                                         )
                wished_product.save()
            else:
                wished_product = Wished(thumb = selected_product.album.all()[:1].get().image,
                                         product_sku = selected_product.sku,
                                         size_sku = selected_size.sku,
                                         en_name = selected_product.en_title,
                                         fr_name = selected_product.fr_title,
                                         ar_name = selected_product.ar_title,
                                         en_spec = selected_product.en_spec,
                                         fr_spec = selected_product.fr_spec,
                                         ar_spec = selected_product.ar_spec,
                                         en_detail = selected_size.en_title,
                                         fr_detail = selected_size.fr_title,
                                         ar_detail = selected_size.ar_title,
                                         )
                wished_product.save()
        else:
            wished_product = Wished(thumb=selected_product.album.all()[:1].get().image,
                                     product_sku=selected_product.sku,
                                     size_sku=selected_product.sku,
                                     en_name=selected_product.en_title,
                                     fr_name=selected_product.fr_title,
                                     ar_name=selected_product.ar_title,
                                     en_spec=selected_product.en_spec,
                                     fr_spec=selected_product.fr_spec,
                                     ar_spec=selected_product.ar_spec,
                                     )
            wished_product.save()
        if not user.wished.filter(product_sku=wished_product.product_sku).exists():
            user.wished.add(wished_product)
            request.session['wish_it_message'] = 'success'
        else:
            request.session['wish_it_message'] = 'exists'

        return redirect('single-product' ,sku ,size_sku)

    else:
        return redirect ('login-page')

def un_wish_it(request, sku):
    if request.user.is_authenticated:
        user = request.user
        selected_product = user.wished.all().get(product_sku=sku)
        selected_product.delete()
        return redirect('wished-products-page')