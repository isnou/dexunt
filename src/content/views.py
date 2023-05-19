from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from products.models import Product, Variant, Option, Feature, Album
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
        url = direction + "/management/admin/products/products-list.html"
        all_products = Product.objects.all()
        product_form = ProductForm()
        context = {
            'nav_side': 'products',
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
            url = direction + "/management/admin/products/selected-product.html"
            product_id = request.POST.get('product_id', False)

            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            context = {
                'nav_side': 'products',
                'selected_product': selected_product,
                'selected_product_form': selected_product_form,
            }
            return render(request, url, context)
        else:
            url = direction + "/management/admin/products/selected-product.html"
            product_id = request.session.get('product_id_token')
            request.session['product_id_token'] = None

            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            context = {
                'nav_side': 'products',
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
            request.session['product_id_token'] = product_id
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, request.FILES, instance=selected_product)
            selected_product_form.save()
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
            url = direction + "/management/admin/products/selected-variant.html"
            product_id = request.POST.get('product_id', False)
            variant_id = request.POST.get('variant_id', False)

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_product = Product.objects.all().get(id=product_id)
            request.session['product_id_token'] = product_id
            context = {
                'nav_side': 'products',
                'selected_variant': selected_variant,
                'selected_product': selected_product
            }
            return render(request, url, context)
        else:
            url = direction + "/management/admin/products/selected-variant.html"
            product_id = request.session.get('product_id_token')
            variant_id = request.session.get('variant_id_token')
            request.session['variant_id_token'] = None

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_product = Product.objects.all().get(id=product_id)
            context = {
                'nav_side': 'products',
                'selected_variant': selected_variant,
                'selected_product': selected_product,
            }
            return render(request, url, context)
    # -----
    if action == 'edit_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)

            en_spec = request.POST.get('en_spec', False)
            fr_spec = request.POST.get('fr_spec', False)
            ar_spec = request.POST.get('ar_spec', False)
            price = request.POST.get('price', False)
            discount = request.POST.get('discount', False)

            selected_variant = Variant.objects.all().get(id=variant_id)

            if price:
                if price[len(price)-3:] == '.00':
                    price = int(price[:-3])
                else:
                    price = int(price)
            else:
                price = None

            if discount:
                if discount[len(discount)-3:] == '.00':
                    discount = int(discount[:-3])
                else:
                    discount = int(discount)

                if discount > price:
                    discount = None
            else:
                discount = None


            selected_variant.en_spec = en_spec
            selected_variant.fr_spec = fr_spec
            selected_variant.ar_spec = ar_spec
            selected_variant.price = price
            selected_variant.discount = discount

            selected_variant.save()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'add_image':
        if request.method == 'POST':
            product_id = request.session.get('product_id_token')
            variant_id = request.POST.get('variant_id', False)
            image = request.FILES.get('image', False)

            selected_product = Product.objects.all().get(id=product_id)
            selected_variant = Variant.objects.all().get(id=variant_id)
            request.session['variant_id_token'] = variant_id
            album = Album(file_name= selected_product.en_title + '/' + selected_variant.en_spec,
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
    # -----
    if action == 'add_option':
        if request.method == 'POST':
            product_id = request.session.get('product_id_token')
            variant_id = request.POST.get('variant_id', False)
            image = request.FILES.get('option_image', False)
            en_value = request.POST.get('en_value', False)
            fr_value = request.POST.get('fr_value', False)
            ar_value = request.POST.get('ar_value', False)
            cost = request.POST.get('cost', False)
            price = request.POST.get('price', False)
            discount = request.POST.get('discount', False)
            quantity = request.POST.get('quantity', False)
            max_quantity = request.POST.get('max_quantity', False)
            delivery_quotient = request.POST.get('delivery_quotient', False)
            points = request.POST.get('points', False)

            selected_product = Product.objects.all().get(id=product_id)
            selected_variant = Variant.objects.all().get(id=variant_id)
            request.session['variant_id_token'] = variant_id
            if image:
                has_image = True
            else:
                has_image = False
            if cost:
                cost = int(cost)
            else:
                cost = None
            if price:
                if price[len(price)-3:] == '.00':
                    price = int(price[:-3])
                else:
                    price = int(price)
            else:
                price = 0
            if discount:
                if discount[len(discount)-3:] == '.00':
                    discount = int(discount[:-3])
                else:
                    discount = int(discount)
            else:
                discount = 0
            if quantity:
                quantity = int(quantity)
            else:
                quantity = None
            if max_quantity:
                max_quantity = int(max_quantity)
            else:
                max_quantity = None
            if delivery_quotient:
                delivery_quotient = int(delivery_quotient)
            else:
                delivery_quotient = None
            if points:
                points = int(points)
            else:
                points = None

            option = Option(file_name= selected_product.en_title + '/' + selected_variant.en_spec + '/' + en_value,
                            image=image,
                            has_image=has_image,
                            en_value=en_value,
                            fr_value=fr_value,
                            ar_value=ar_value,
                            product_token=selected_product.product_token,
                            cost=cost,
                            price=price,
                            discount=discount,
                            )
            if delivery_quotient:
                option.delivery_quotient = delivery_quotient
            if quantity:
                option.quantity = quantity
            if max_quantity:
                option.max_quantity = max_quantity
            if points:
                option.points = points
            option.save()
            selected_variant.option.add(option)

            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'delete_option':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            option_id = request.POST.get('option_id', False)

            option = Option.objects.all().get(id=option_id)
            option.delete()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'edit_option':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            option_id = request.POST.get('option_id', False)
            image = request.FILES.get('option_image', False)
            en_value = request.POST.get('en_value', False)
            fr_value = request.POST.get('fr_value', False)
            ar_value = request.POST.get('ar_value', False)
            cost = request.POST.get('cost', False)
            price = request.POST.get('price', False)
            discount = request.POST.get('discount', False)
            quantity = request.POST.get('quantity', False)
            max_quantity = request.POST.get('max_quantity', False)
            delivery_quotient = request.POST.get('delivery_quotient', False)
            points = request.POST.get('points', False)

            selected_option = Option.objects.all().get(id=option_id)

            if cost:
                if cost[len(cost)-3:] == '.00':
                    cost = int(cost[:-3])
                else:
                    cost = int(cost)
            else:
                cost = 0

            if price:
                if price[len(price)-3:] == '.00':
                    price = int(price[:-3])
                else:
                    price = int(price)
            else:
                price = 0

            if discount:
                if discount[len(discount)-3:] == '.00':
                    discount = int(discount[:-3])
                else:
                    discount = int(discount)
            else:
                discount = 0

            if quantity:
                if quantity[len(quantity)-3:] == '.00':
                    quantity = int(quantity[:-3])
                else:
                    quantity = int(quantity)
            else:
                quantity = 0

            if max_quantity:
                if max_quantity[len(max_quantity)-3:] == '.00':
                    max_quantity = int(max_quantity[:-3])
                else:
                    max_quantity = int(max_quantity)
            else:
                max_quantity = 0

            if delivery_quotient:
                if delivery_quotient[len(delivery_quotient)-3:] == '.00':
                    delivery_quotient = int(delivery_quotient[:-3])

                    if delivery_quotient > 100:
                        delivery_quotient = 100
                    if delivery_quotient < 0:
                        delivery_quotient = 0
                else:
                    delivery_quotient = int(delivery_quotient)
            else:
                delivery_quotient = 100

            if points:
                if points[len(points)-3:] == '.00':
                    points = int(points[:-3])
                else:
                    points = int(points)
            else:
                points = 0

            if image:
                selected_option.image = image
            selected_option.en_value = en_value
            selected_option.fr_value = fr_value
            selected_option.ar_value = ar_value
            selected_option.cost = cost
            selected_option.price = price
            selected_option.discount = discount
            selected_option.quantity = quantity
            selected_option.max_quantity = max_quantity
            selected_option.delivery_quotient = delivery_quotient
            selected_option.points = points

            selected_option.save()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'convert_option':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            option_id = request.POST.get('option_id', False)

            option = Option.objects.all().get(id=option_id)
            if option.has_image:
                option.has_image = False
            else:
                option.has_image = True
            option.save()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'add_feature':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)

            en_title = request.POST.get('feature_en_title', False)
            fr_title = request.POST.get('feature_fr_title', False)
            ar_title = request.POST.get('feature_ar_title', False)
            en_value = request.POST.get('feature_en_value', False)
            fr_value = request.POST.get('feature_fr_value', False)
            ar_value = request.POST.get('feature_ar_value', False)

            selected_variant = Variant.objects.all().get(id=variant_id)
            request.session['variant_id_token'] = variant_id


            feature = Feature(en_title=en_title,
                              fr_title=fr_title,
                              ar_title=ar_title,
                              en_value=en_value,
                              fr_value=fr_value,
                              ar_value=ar_value,
                              )
            feature.save()
            selected_variant.feature.add(feature)

            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'delete_feature':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            feature_id = request.POST.get('feature_id', False)

            selected_feature = Feature.objects.all().get(id=feature_id)
            selected_feature.delete()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')
    # -----
    if action == 'edit_feature':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            feature_id = request.POST.get('feature_id', False)

            en_title = request.POST.get('feature_en_title', False)
            fr_title = request.POST.get('feature_fr_title', False)
            ar_title = request.POST.get('feature_ar_title', False)
            en_value = request.POST.get('feature_en_value', False)
            fr_value = request.POST.get('feature_fr_value', False)
            ar_value = request.POST.get('feature_ar_value', False)

            selected_feature = Feature.objects.all().get(id=feature_id)

            selected_feature.en_title = en_title
            selected_feature.fr_title = fr_title
            selected_feature.ar_title = ar_title

            selected_feature.en_value = en_value
            selected_feature.fr_value = fr_value
            selected_feature.ar_value = ar_value

            selected_feature.save()

            request.session['variant_id_token'] = variant_id
            return redirect('products-menu', 'view_variant')


def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')