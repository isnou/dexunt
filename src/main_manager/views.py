from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from main_manager.models import Product, Variant, Option, Feature, Album, FlashProduct
from main_manager.forms import ProductForm, VariantForm, FeatureForm, OptionForm, FlashForm
from authentication.models import User


def admin_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # ----- main page ------------
    if action == 'main':
        url = direction + "/management/admin/home.html"
        context = {
            'nav_side': 'home'
        }
        return render(request, url, context)

def manage_showcase(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/showcase/grid.html"
        all_products = Variant.objects.all()
        all_flash_products = FlashProduct.objects.all()

        published_products = all_products.exclude(is_activated=False)
        unpublished_products = all_products.exclude(is_activated=True)

        published_flash_products = all_flash_products.exclude(is_activated=False)
        unpublished_flash_products = all_flash_products.exclude(is_activated=True)

        context = {
            'nav_side': 'showcase',
            'all_products': all_products,
            'all_flash_products': all_flash_products,
            'published_products': published_products,
            'unpublished_products': unpublished_products,
            'published_flash_products': published_flash_products,
            'unpublished_flash_products': unpublished_flash_products,
        }
        return render(request, url, context)
    # -----
    if action == 'publish_products':
        if request.method == 'POST':
            product_ids = request.POST.getlist('product_ids')
            for product_id in product_ids:
                selected_product = Product.objects.all().get(id=product_id)
                selected_product.is_activated = True
                selected_product.save()
                selected_product.check_availability()
            return redirect('manage-showcase', 'main')
    if action == 'publish_flash_products':
        if request.method == 'POST':
            product_ids = request.POST.getlist('product_ids')
            for product_id in product_ids:
                selected_product = FlashProduct.objects.all().get(id=product_id)
                selected_product.is_activated = True
                selected_product.save()
                selected_product.clean()
            return redirect('manage-showcase', 'main')

def manage_products(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- all products ---------------- #
    if action == 'main':
        url = direction + "/management/admin/products/list.html"
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
            new_product_form = ProductForm(request.POST)
            if new_product_form.is_valid():
                new_product_form.save()
                return redirect('manage-products', 'main')
    # -----
    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.delete()
            return redirect('manage-products', 'main')
    # --------------- selected product ------------ #
    if action == 'view_product':
        if request.method == 'POST':
            url = direction + "/management/admin/products/selected.html"
            product_id = request.POST.get('product_id', False)

            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)

            variant_form = VariantForm()
            context = {
                'nav_side': 'products',
                'selected_product': selected_product,
                'selected_product_form': selected_product_form,
                'variant_form': variant_form,
            }
            return render(request, url, context)
        else:
            url = direction + "/management/admin/products/selected.html"
            product_id = request.session.get('product_id_token')
            request.session['product_id_token'] = None

            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            variant_form = VariantForm()
            context = {
                'nav_side': 'products',
                'selected_product': selected_product,
                'selected_product_form': selected_product_form,
                'variant_form': variant_form,
            }
            return render(request, url, context)
    # -----
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            request.session['product_id_token'] = product_id
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('manage-products', 'view_product')
    # -----
    if action == 'add_new_variant':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            request.session['product_id_token'] = product_id
            selected_product = Product.objects.all().get(id=product_id)
            new_variant = Variant(en_title=selected_product.en_title,
                                  fr_title=selected_product.fr_title,
                                  ar_title=selected_product.ar_title,
                                  en_spec='unlinked variant',
                                  product_token=selected_product.product_token,
                                  )
            new_variant.save()

            selected_variant_form = VariantForm(request.POST, instance=new_variant)
            selected_variant_form.save()

            selected_product.variant.add(new_variant)
            return redirect('manage-products', 'view_product')
    # -----
    if action == 'delete_variant':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant.delete()

            request.session['product_id_token'] = product_id
            return redirect('manage-products', 'view_product')
    # --------------- selected variant ------------ #
    if action == 'view_variant':
        if request.method == 'POST':
            url = direction + "/management/admin/products/selected-variant.html"
            product_id = request.POST.get('product_id', False)
            variant_id = request.POST.get('variant_id', False)

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_product = Product.objects.all().get(id=product_id)
            selected_variant.check_availability()

            request.session['product_id_token'] = product_id
            variant_form = VariantForm()
            feature_form = FeatureForm()
            option_form = OptionForm()
            context = {
                'nav_side': 'products',
                'selected_variant': selected_variant,
                'selected_product': selected_product,
                'variant_form': variant_form,
                'feature_form': feature_form,
                'option_form': option_form,
            }
            return render(request, url, context)
        else:
            url = direction + "/management/admin/products/selected-variant.html"
            product_id = request.session.get('product_id_token')
            variant_id = request.session.get('variant_id_token')
            request.session['variant_id_token'] = None

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_product = Product.objects.all().get(id=product_id)
            selected_variant.check_availability()

            variant_form = VariantForm()
            feature_form = FeatureForm()
            option_form = OptionForm()
            context = {
                'nav_side': 'products',
                'selected_variant': selected_variant,
                'selected_product': selected_product,
                'variant_form': variant_form,
                'feature_form': feature_form,
                'option_form': option_form,
            }
            return render(request, url, context)
    # -----
    if action == 'edit_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)

            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant_form = VariantForm(request.POST, instance=selected_variant)
            selected_variant_form.save()

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
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

            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'delete_image':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            album_id = request.POST.get('album_id', False)

            album = Album.objects.all().get(id=album_id)
            album.delete()

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'add_feature':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            new_feature = Feature(en_name='unlinked feature',
                                  )
            new_feature.save()
            selected_feature_form = FeatureForm(request.POST, instance=new_feature)
            selected_feature_form.save()
            selected_variant.feature.add(new_feature)
            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'delete_feature':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            feature_id = request.POST.get('feature_id', False)

            selected_feature = Feature.objects.all().get(id=feature_id)
            selected_feature.delete()

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'edit_feature':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            feature_id = request.POST.get('feature_id', False)
            selected_feature = Feature.objects.all().get(id=feature_id)

            selected_feature_form = FeatureForm(request.POST, instance=selected_feature)
            selected_feature_form.save()

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'add_option':
        if request.method == 'POST':
            product_id = request.session.get('product_id_token')
            variant_id = request.POST.get('variant_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_variant = Variant.objects.all().get(id=variant_id)

            new_option = Option(file_name= selected_product.en_title + '/' + selected_variant.en_spec,
                                product_token=selected_product.product_token,
                                )
            new_option.save()
            selected_option_form = OptionForm(request.POST, request.FILES, instance=new_option)
            selected_option_form.save()
            selected_variant.option.add(new_option)

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'delete_option':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            option_id = request.POST.get('option_id', False)

            option = Option.objects.all().get(id=option_id)
            option.delete()

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
    # -----
    if action == 'edit_option':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            option_id = request.POST.get('option_id', False)
            selected_option = Option.objects.all().get(id=option_id)

            selected_option_form = OptionForm(request.POST, request.FILES, instance=selected_option)
            selected_option_form.save()

            request.session['variant_id_token'] = variant_id
            return redirect('manage-products', 'view_variant')
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
            return redirect('manage-products', 'view_variant')

def manage_flash(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/flash/list.html"
        all_products = Product.objects.all()
        all_flash_products = FlashProduct.objects.all()
        flash_form = FlashForm()

        context = {
            'nav_side': 'flash',
            'all_products': all_products,
            'all_flash_products': all_flash_products,
            'flash_form': flash_form,
        }
        return render(request, url, context)
    # -----
    if action == 'link_products':
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            variant_id = request.POST.get('variant_id')
            option_id = request.POST.get('option_id')

            selected_product = Product.objects.all().get(id=product_id)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_option = Option.objects.all().get(id=option_id)

            if selected_option.has_image:
                image = selected_option.image
            else:
                album = selected_variant.album.all()[0]
                image = album.image

            FlashProduct(en_title=selected_variant.en_title,
                         fr_title=selected_variant.fr_title,
                         ar_title=selected_variant.ar_title,

                         en_spec=selected_variant.en_spec,
                         fr_spec=selected_variant.fr_spec,
                         ar_spec=selected_variant.ar_spec,

                         en_value=selected_option.en_value,
                         fr_value=selected_option.fr_value,
                         ar_value=selected_option.ar_value,

                         image=image,
                         product_token=selected_product.product_token,
                         upc=selected_option.upc,
                         cost=selected_option.cost,
                         price=selected_option.price,
                         ).save()
            return redirect('manage-flash', 'main')
    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = FlashProduct.objects.all().get(id=product_id)
            selected_option = Option.objects.all().get(upc=selected_product.upc)
            selected_option.quantity += selected_product.quantity
            selected_option.is_activated = True
            selected_option.save()
            selected_product.delete()
            return redirect('manage-flash', 'main')
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            quantity = int(request.POST.get('quantity', False))
            selected_product = FlashProduct.objects.all().get(id=product_id)
            selected_option = Option.objects.all().get(upc=selected_product.upc)

            if quantity > selected_option.quantity:
                selected_product.quantity=selected_option.quantity
                selected_option.quantity=0
            else:
                selected_product.quantity=quantity
                selected_option.quantity-=quantity

            selected_product.save()
            selected_option.is_activated = False
            selected_option.save()

            flash_form = FlashForm(request.POST, request.FILES, instance=selected_product)
            if flash_form.is_valid():
                flash_form.save()
                return redirect('manage-flash', 'main')

