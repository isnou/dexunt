from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from products.models import Product, Variant, Album
from products.forms import ProductForm



def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    url = direction + "/home/main-page.html"
    login_form = LoginForm()
    signup_form = SignupForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, url, context)


def management_page(request, action):
    if action == 'statistics':
        return redirect('statistics-menu', 'main')
    if action == 'products':
        return redirect('products-menu', 'main')


def statistics_menu(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # ----- main page ------------
    if action == 'main':
        url = direction + "/management/admin/statistics.html"
        context = {
            'nav_side': 'statistics'
        }
        return render(request, url, context)


def products_menu(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # ----- main page ------------
    if action == 'main':
        url = direction + "/management/admin/products.html"
        all_products = Product.objects.all()
        product_form = ProductForm()
        context = {
            'nav_side': 'products',
            'show': 'all_products',
            'all_products': all_products,
            'product_form': product_form,
        }
        return render(request, url, context)
    # -----
    if action == 'add_new_product':
        if request.method == 'POST':
            completed_product_form = ProductForm(request.POST, request.FILES)
            if completed_product_form.is_valid():
                completed_product_form.save()
                return redirect('products-menu', 'main')
    # -----
    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.delete()
            return redirect('products-menu', 'main')
    # ----- product page ---------
    if action == 'view_product':
        if request.method == 'POST':
            url = direction + "/management/admin/products.html"
            product_id = request.POST.get('product_id', False)

            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            context = {
                'nav_side': 'products',
                'show': 'selected_product',
                'selected_product': selected_product,
                'selected_product_form': selected_product_form,
            }
            return render(request, url, context)
        else:
            url = direction + "/management/admin/products.html"
            product_id = request.session.get('product_id_token')
            request.session['product_id_token'] = None

            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            context = {
                'nav_side': 'products',
                'show': 'selected_product',
                'selected_product': selected_product,
                'selected_product_form': selected_product_form,
            }
            return render(request, url, context)
    # -----
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            request.session['product_id_token'] = product_id
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, request.FILES, instance=selected_product)
            selected_product_form.save()
            return redirect('products-menu', 'view_product')
    # -----
    if action == 'add_new_variant':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)

            en_spec = request.POST.get('en_spec', False)
            fr_spec = request.POST.get('fr_spec', False)
            ar_spec = request.POST.get('ar_spec', False)
            price = request.POST.get('price', False)
            discount = request.POST.get('discount', False)

            price = int(price)
            discount = int(discount)
            if discount > price:
                discount = None

            request.session['product_id_token'] = product_id
            selected_product = Product.objects.all().get(id=product_id)
            selected_variant = Variant(en_spec=en_spec,
                                       fr_spec=fr_spec,
                                       ar_spec=ar_spec,
                                       price=price,
                                       discount=discount)
            selected_variant.product_token = selected_product.product_token
            selected_variant.save()
            selected_product.variant.add(selected_variant)

            return redirect('products-menu', 'view_product')
    # -----
    if action == 'delete_variant':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant.delete()

            request.session['product_id_token'] = product_id
            return redirect('products-menu', 'view_product')
    # ----- variant page ---------
    if action == 'view_variant':
        if request.method == 'POST':
            url = direction + "/management/admin/products.html"
            product_id = request.POST.get('product_id', False)
            variant_id = request.POST.get('variant_id', False)

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_product = Product.objects.all().get(id=product_id)
            request.session['product_id_token'] = product_id
            context = {
                'nav_side': 'products',
                'show': 'selected_variant',
                'selected_variant': selected_variant,
                'selected_product': selected_product
            }
            return render(request, url, context)
        else:
            url = direction + "/management/admin/products.html"
            product_id = request.session.get('product_id_token')
            variant_id = request.session.get('variant_id_token')
            request.session['variant_id_token'] = None

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_product = Product.objects.all().get(id=product_id)
            context = {
                'nav_side': 'products',
                'show': 'selected_variant',
                'selected_variant': selected_variant,
                'selected_product': selected_product,
            }
            return render(request, url, context)
    # -----
    if action == 'edit_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'add_image':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            image = request.FILES.get('image', False)

            selected_variant = Variant.objects.all().get(id=variant_id)
            request.session['variant_id_token'] = variant_id
            album = Album(file_name=selected_variant.en_spec,
                          image=image,
                          )
            album.save()
            selected_variant.album.add(album)

            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'delete_image':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            album_id = request.POST.get('album_id', False)

            album = Album.objects.all().get(id=album_id)
            album.delete()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')



def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')