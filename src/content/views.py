from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from products.models import Product
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
    if action == 'add_new_product':
        if request.method == 'POST':
            completed_product_form = ProductForm(request.POST, request.FILES)
            if completed_product_form.is_valid():
                completed_product_form.save()
                return redirect('products-menu', 'main')
    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.delete()
            return redirect('products-menu', 'main')
    if action == 'view_product':
        if request.method == 'POST':
            url = direction + "/management/admin/products.html"
            if request.session.get('selected_product_id', None):
                product_id = request.session.get('selected_product_id')
                request.session['selected_product_id'] = None
            else:
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
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            request.session['selected_product_id'] = product_id
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('products-menu', 'view_product')



def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')