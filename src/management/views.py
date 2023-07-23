from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from add_ons import functions
from django.utils import timezone
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from .models import Product, Variant, Option, Feature, Album, FlashProduct ,Description, Store
from .forms import ProductForm, VariantForm, FeatureForm, OptionForm, FlashForm ,DescriptionForm ,StoreForm
from home.forms import ProvinceForm, MunicipalityForm, CouponForm
from home.models import Province, Municipality, Coupon, Order
from authentication.models import User, users_filter, change_role
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from authentication.forms import UpdateProfileForm, UpdateProfilePhotoForm



# ------------------------------- Admin -------------------------------- #
@login_required
@permission_required('main_manager.delete_option')
def admin_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/home.html"
        all_products = Variant.objects.all()
        all_flash_products = FlashProduct.objects.all()

        published_products = all_products.exclude(is_activated=False)
        unpublished_products = all_products.exclude(is_activated=True)

        published_flash_products = all_flash_products.exclude(is_activated=False)
        unpublished_flash_products = all_flash_products.exclude(is_activated=True)
        context = {
            'nav_side': 'home',
            'all_products': all_products,
            'all_flash_products': all_flash_products,
            'published_products': published_products,
            'unpublished_products': unpublished_products,
            'published_flash_products': published_flash_products,
            'unpublished_flash_products': unpublished_flash_products,
        }
        return render(request, url, context)
#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_users(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 6

    # -- main page -- #
    if action == 'main':
        url = direction + "/management/admin/users/list.html"
        users_list = User.objects.all().exclude(username=request.user.username)

        if request.GET.get('init', None):
            request.session['users_key_word']=None

        if request.session.get('users_key_word', None):
            users_list = users_list.filter(tags__icontains=request.session.get('users_key_word'))
            search_key_word = request.session.get('users_key_word')
        else:
            search_key_word = None

        new_filter = request.GET.get('filter', None)
        if not request.session.get('users_filter', None):
            request.session['users_filter'] = 'all'

        users_list = users_filter(request, users_list, new_filter)
        filtered = request.session.get('users_filter', None)

        if not request.session.get('users-page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('users-page')
            request.session['users-page'] = None

        paginator = Paginator(users_list, items_by_page)
        try:
            users_list = paginator.page(page)
        except PageNotAnInteger:
            users_list = paginator.page(1)
        except EmptyPage:
            users_list = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'users',
            'search_key_word': search_key_word,
            'filtered': filtered,
            'users_list': users_list,
        }
        return render(request, url, context)
    # -- main page actions -- #
    if action == 'activate_user':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            users_page = request.POST.get('users_page', False)
            request.session['users-page'] = users_page
            selected_user = User.objects.all().get(id=user_id)
            selected_user.is_activated = True
            selected_user.save()
            return redirect ('admin-manage-users', 'main')
    if action == 'deactivate_user':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            users_page = request.POST.get('users_page', False)
            request.session['users-page'] = users_page
            selected_user = User.objects.all().get(id=user_id)
            selected_user.is_activated = False
            selected_user.save()
            return redirect ('admin-manage-users', 'main')
    if action == 'delete_user':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            users_page = request.POST.get('users_page', False)
            request.session['users-page'] = users_page
            selected_user = User.objects.all().get(id=user_id)
            selected_user.delete()
            return redirect ('admin-manage-users', 'main')
    if action == 'change_user':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            role = request.POST.get('role', False)
            selected_user = User.objects.all().get(id=user_id)
            change_role(selected_user, role)
            return redirect ('admin-manage-users', 'main')
    # -- search partial show -- #
    if action == 'search_users':
        url = direction + "/management/admin/users/partial-list.html"
        key_word = request.GET.get('key_word', None)

        if key_word:
            request.session['users_key_word'] = key_word
        else:
            request.session['users_key_word'] = None

        users_list = User.objects.values().filter(tags__icontains=key_word).exclude(username=request.user.username)

        new_filter = request.GET.get('filter', None)
        if not request.session.get('users_filter', None):
            request.session['users_filter'] = 'all'

        users_list = users_filter(request, users_list, new_filter)

        if not request.session.get('users-page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('users-page')
            request.session['users-page'] = None

        paginator = Paginator(users_list, items_by_page)
        try:
            users_list = paginator.page(page)
        except PageNotAnInteger:
            users_list = paginator.page(1)
        except EmptyPage:
            users_list = paginator.page(paginator.num_pages)

        context = {
            'users_list': users_list,
        }
        return render(request, url, context)
    # -- selected item page show -- #
    if action == 'select_user':
        url = direction + "/management/admin/users/selected.html"
        if request.session.get('user_id', None):
            user_id = request.session.get('user_id')
            request.session['user_id'] = None
        else:
            user_id = request.GET.get('user_id', None)
        selected_user = User.objects.all().get(id=user_id)

        context = {
            'nav_side': 'users',
            'selected_user': selected_user,
        }
        return render(request, url, context)
#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_stores(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 6

    # -- main page -- #
    if action == 'main':
        url = direction + "/management/admin/stores/list.html"
        stores = Store.objects.all()

        if request.GET.get('init', None):
            request.session['stores_key_word']=None

        if request.session.get('stores_key_word', None):
            stores = stores.filter(tags__icontains=request.session.get('stores_key_word'))
            search_key_word = request.session.get('stores_key_word')
        else:
            search_key_word = None

        new_filter = request.GET.get('filter', None)
        if not request.session.get('stores_filter', None):
            request.session['stores_filter'] = 'all'

        stores = users_filter(request, stores, new_filter)
        filtered = request.session.get('stores_filter', None)

        if not request.session.get('stores-page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('stores-page')
            request.session['stores-page'] = None

        paginator = Paginator(stores, items_by_page)
        try:
            stores = paginator.page(page)
        except PageNotAnInteger:
            stores = paginator.page(1)
        except EmptyPage:
            stores = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'stores',
            'search_key_word': search_key_word,
            'filtered': filtered,
            'stores': stores,
        }
        return render(request, url, context)
    # -- main page actions -- #
    if action == 'delete_store':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            users_page = request.POST.get('users_page', False)
            request.session['users-page'] = users_page
            selected_user = User.objects.all().get(id=user_id)
            selected_user.delete()
            return redirect ('admin-manage-users', 'main')
    if action == 'edit_store':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            role = request.POST.get('role', False)
            selected_user = User.objects.all().get(id=user_id)
            change_role(selected_user, role)
            return redirect ('admin-manage-users', 'main')
#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_products(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/products/list.html"
        request.session['variant_id_token'] = None
        request.session['product_id_token'] = None

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        all_products = Product.objects.all()
        if all_products.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 6)
        try:
            all_products = paginator.page(page)
        except PageNotAnInteger:
            all_products = paginator.page(1)
        except EmptyPage:
            all_products = paginator.page(paginator.num_pages)

        product_form = ProductForm()
        variant_form = VariantForm()
        option_form = OptionForm()
        context = {
            'nav_side': 'products',
            'all_products': all_products,
            'paginate': paginate,
            'product_form': product_form,
            'variant_form': variant_form,
            'option_form': option_form,
            'errors': errors,
        }
        return render(request, url, context)
    if action == 'add_new_product':
        if request.method == 'POST':
            new_option = Option()
            new_option.save()
            new_variant = Variant()
            new_variant.save()
            new_product = Product()
            new_product.save()
            new_product_form = ProductForm(request.POST, instance=new_product)
            new_variant_form = VariantForm(request.POST, instance=new_variant)
            new_option_form = OptionForm(request.POST, instance=new_option)

            if new_product_form.is_valid():
                new_product_form.save()
                new_product.set_variant(new_variant)
                if new_variant_form.is_valid():
                    new_variant_form.save()
                    if new_option_form.is_valid():
                        new_option_form.save()
                        new_variant.set_option(new_option)
                        request.session['product_id_token'] = new_product.id
                        request.session['variant_id_token'] = new_variant.id
                        return redirect('admin-manage-products', 'view_variant')
                    else:
                        request.session['error_messages'] = new_option_form.errors
                else:
                    request.session['error_messages'] = new_variant_form.errors
            else:
                request.session['error_messages'] = new_product_form.errors

            if not new_product_form.is_valid() or not new_variant_form.is_valid() or not new_option_form.is_valid():
                new_product.delete()
                new_variant.delete()
                new_option.delete()
                return redirect('admin-manage-products', 'main')

    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.delete()
            return redirect('admin-manage-products', 'main')
    if action == 'clean_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)

            for variant in selected_product.variant.all():
                for option in variant.option.all():
                    if FlashProduct.objects.all().filter(upc=option.upc).exists():
                        if not FlashProduct.objects.all().get(upc=option.upc).is_activated:
                            option.is_activated = True
                            option.save()
                        else:
                            option.is_activated = False
                            option.save()
                    else:
                        option.is_activated = True
                        option.save()
                variant.is_activated = True
                variant.clean()

            return redirect('admin-manage-products', 'main')
    # --------------- selected product ------------ #
    if action == 'view_product':
        url = direction + "/management/admin/products/selected.html"
        request.session['variant_id_token'] = None
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            request.session['product_id_token'] = product_id
        else:
            product_id = request.session.get('product_id_token')

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
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            selected_product_form.save()
            selected_product.update()
            return redirect('admin-manage-products', 'view_product')
    if action == 'duplicate_variant':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            variant_id = request.POST.get('variant_id', None)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant.duplicate()
            return redirect('admin-manage-products', 'view_product')
    if action == 'add_new_variant':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            new_variant = Variant(en_title=selected_product.en_title,
                                  fr_title=selected_product.fr_title,
                                  ar_title=selected_product.ar_title,
                                  brand=selected_product.brand,
                                  en_spec='unlinked variant',
                                  product_token=selected_product.product_token,
                                  )
            new_variant.save()

            selected_variant_form = VariantForm(request.POST, instance=new_variant)
            selected_variant_form.save()

            selected_product.variant.add(new_variant)
            return redirect('admin-manage-products', 'view_product')
    if action == 'delete_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant.delete()
            return redirect('admin-manage-products', 'view_product')

    # --------------- selected variant ------------ #
    if action == 'view_variant':
        url = direction + "/management/admin/products/selected-variant.html"
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            variant_id = request.POST.get('variant_id', False)
            request.session['variant_id_token'] = variant_id
        else:
            product_id = request.session.get('product_id_token')
            variant_id = request.session.get('variant_id_token')

        selected_variant = Variant.objects.all().get(id=variant_id)
        selected_product = Product.objects.all().get(id=product_id)
        selected_variant.clean()

        variant_form = VariantForm()
        option_form = OptionForm()
        feature_form = FeatureForm()
        description_form = DescriptionForm()
        context = {
            'nav_side': 'products',
            'selected_variant': selected_variant,
            'selected_product': selected_product,
            'variant_form': variant_form,
            'option_form': option_form,
            'feature_form': feature_form,
            'description_form': description_form,
        }
        return render(request, url, context)
    if action == 'edit_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant_form = VariantForm(request.POST, instance=selected_variant)
            selected_variant_form.save()

            return redirect('admin-manage-products', 'view_variant')
    if action == 'add_image':
        if request.method == 'POST':
            product_id = request.session.get('product_id_token')
            variant_id = request.POST.get('variant_id', False)
            image = request.FILES.get('image', False)

            selected_product = Product.objects.all().get(id=product_id)
            selected_variant = Variant.objects.all().get(id=variant_id)
            album = Album(file_name= selected_product.en_title + '/' + selected_variant.en_spec,
                          image=image,
                          )
            album.save()
            selected_variant.album.add(album)

            return redirect('admin-manage-products', 'view_variant')

    if action == 'add_images':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            variant_id = request.POST.get('variant_id', None)
            request.session['variant_id_token'] = variant_id
            selected_variant = Variant.objects.all().get(id=variant_id)
            album = Album(file_name=selected_variant.en_title + '/' + selected_variant.en_spec + '/',
                          image=request.FILES.get('variant_image'),
                          )
            album.save()
            selected_variant.album.add(album)
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_image':
        if request.method == 'POST':
            album_id = request.POST.get('album_id', False)

            album = Album.objects.all().get(id=album_id)
            album.delete()
            return redirect('admin-manage-products', 'view_variant')

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
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_feature':
        if request.method == 'POST':
            feature_id = request.POST.get('feature_id', False)

            selected_feature = Feature.objects.all().get(id=feature_id)
            selected_feature.delete()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'edit_feature':
        if request.method == 'POST':
            feature_id = request.POST.get('feature_id', False)
            selected_feature = Feature.objects.all().get(id=feature_id)

            selected_feature_form = FeatureForm(request.POST, instance=selected_feature)
            selected_feature_form.save()
            return redirect('admin-manage-products', 'view_variant')

    if action == 'add_description':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            new_description = Description()
            new_description.save()
            selected_description_form = DescriptionForm(request.POST, instance=new_description)
            selected_description_form.save()
            selected_variant.description.add(new_description)
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_description':
        if request.method == 'POST':
            description_id = request.POST.get('description_id', False)
            selected_description = Description.objects.all().get(id=description_id)
            selected_description.delete()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'edit_description':
        if request.method == 'POST':
            description_id = request.POST.get('description_id', False)
            selected_description = Description.objects.all().get(id=description_id)
            selected_description_form = DescriptionForm(request.POST, instance=selected_description)
            selected_description_form.save()
            return redirect('admin-manage-products', 'view_variant')

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
            selected_option_form = OptionForm(request.POST, instance=new_option)
            selected_option_form.save()
            selected_variant.option.add(new_option)
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_option':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            request.session['variant_id_token'] = request.POST.get('variant_id', None)
            option_id = request.POST.get('option_id', False)

            option = Option.objects.all().get(id=option_id)
            option.delete()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'edit_option':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            request.session['variant_id_token'] = request.POST.get('variant_id', None)
            option_id = request.POST.get('option_id', False)
            selected_option = Option.objects.all().get(id=option_id)

            selected_option_form = OptionForm(request.POST, instance=selected_option)
            selected_option_form.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'convert_option':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            request.session['variant_id_token'] = request.POST.get('variant_id', None)
            selected_option = Option.objects.all().get(id=request.POST.get('option_id', False))
            selected_option.has_image = True
            selected_option.image = request.FILES.get('option_image')
            selected_option.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'deconvert_option':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            request.session['variant_id_token'] = request.POST.get('variant_id', None)
            selected_option = Option.objects.all().get(id=request.POST.get('option_id', False))
            selected_option.has_image = False
            selected_option.image = None
            selected_option.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'duplicate_option':
        if request.method == 'POST':
            request.session['product_id_token'] = request.POST.get('product_id', None)
            variant_id = request.POST.get('variant_id', None)
            request.session['variant_id_token'] = variant_id
            option_id = request.POST.get('option_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_option = Option.objects.all().get(id=option_id)
            selected_option.duplicate(selected_variant)
            return redirect('admin-manage-products', 'view_variant')


#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_flash(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/flash/list.html"
        all_products = Product.objects.all()
        all_flash_products = FlashProduct.objects.all()
        if all_flash_products.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(all_flash_products, 6)
        try:
            all_flash_products = paginator.page(page)
        except PageNotAnInteger:
            all_flash_products = paginator.page(1)
        except EmptyPage:
            all_flash_products = paginator.page(paginator.num_pages)

        flash_form = FlashForm()
        context = {
            'nav_side': 'flash',
            'all_products': all_products,
            'all_flash_products': all_flash_products,
            'paginate': paginate,
            'flash_form': flash_form,
        }
        return render(request, url, context)
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

                         file_name= 'flash' + selected_variant.en_title + '/' + selected_variant.en_spec + '/' + selected_option.en_value,
                         image=image,
                         product_token=selected_product.product_token,
                         upc=selected_option.upc,
                         cost=selected_option.cost,
                         price=selected_option.price,
                         ).save()
            return redirect('admin-manage-flash', 'main')
    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = FlashProduct.objects.all().get(id=product_id)
            selected_option = Option.objects.all().get(upc=selected_product.upc)
            selected_option.quantity += selected_product.quantity
            selected_option.is_activated = True
            selected_option.save()
            selected_product.delete()
            return redirect('admin-manage-flash', 'main')
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            quantity = int(request.POST.get('quantity', False))
            selected_product = FlashProduct.objects.all().get(id=product_id)
            selected_option = Option.objects.all().get(upc=selected_product.upc)

            if quantity >= selected_option.quantity:
                selected_product.quantity = selected_option.quantity
            else:
                selected_product.quantity = quantity

            selected_product.save()
            if selected_product.quantity and selected_option.is_activated:
                selected_option.is_activated = False
            selected_option.save()

            flash_form = FlashForm(request.POST, request.FILES, instance=selected_product)
            if flash_form.is_valid():
                flash_form.save()
                return redirect('admin-manage-flash', 'main')
#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_orders(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/orders/list.html"
        all_orders = Order.objects.all().order_by('-updated_at')

        if all_orders.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(all_orders, 6)
        try:
            all_orders = paginator.page(page)
        except PageNotAnInteger:
            all_orders = paginator.page(1)
        except EmptyPage:
            all_orders = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'orders',
            'all_orders': all_orders,
            'paginate': paginate,
        }
        return render(request, url, context)
    if action == 'delete_order':
        if request.method == 'POST':
            order_id = request.POST.get('order_id', False)
            selected_order = Order.objects.all().get(id=order_id)
            selected_order.delete_products()
            selected_order.delete()
            return redirect('admin-manage-orders', 'main')
#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_shipping(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/shipping/provinces.html"
        request.session['province_id_token'] = None
        all_provinces = Province.objects.all()
        if all_provinces.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(all_provinces, 6)
        try:
            all_provinces = paginator.page(page)
        except PageNotAnInteger:
            all_provinces = paginator.page(1)
        except EmptyPage:
            all_provinces = paginator.page(paginator.num_pages)

        province_form = ProvinceForm()
        context = {
            'nav_side': 'shipping',
            'all_provinces': all_provinces,
            'paginate': paginate,
            'province_form': province_form,
        }
        return render(request, url, context)
    if action == 'add_province':
        if request.method == 'POST':
            province_form = ProvinceForm(request.POST)
            if province_form.is_valid():
                province_form.save()
                return redirect('admin-manage-shipping', 'main')
    if action == 'edit_province':
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            selected_province = Province.objects.all().get(id=province_id)
            province_form = ProvinceForm(request.POST, instance=selected_province)
            if province_form.is_valid():
                province_form.save()
                return redirect('admin-manage-shipping', 'main')
    if action == 'delete_province':
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            selected_province = Province.objects.all().get(id=province_id)
            selected_province.delete()
            return redirect('admin-manage-shipping', 'main')
    # --------------- selected province ------------ #
    if action == 'view_province':
        url = direction + "/management/admin/shipping/selected_province.html"
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            request.session['province_id_token'] = province_id
        else:
            province_id = request.session.get('province_id_token')

        selected_province = Province.objects.all().get(id=province_id)
        selected_province_municipalities = selected_province.municipality.all()
        if selected_province_municipalities.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(selected_province_municipalities, 6)
        try:
            selected_province_municipalities = paginator.page(page)
        except PageNotAnInteger:
            selected_province_municipalities = paginator.page(1)
        except EmptyPage:
            selected_province_municipalities = paginator.page(paginator.num_pages)

        selected_province_form = ProvinceForm(request.POST, instance=selected_province)
        municipality_form = MunicipalityForm()
        context = {
            'nav_side': 'shipping',
            'selected_province': selected_province,
            'selected_province_municipalities': selected_province_municipalities,
            'paginate': paginate,
            'selected_province_form': selected_province_form,
            'municipality_form': municipality_form,
        }
        return render(request, url, context)
    if action == 'add_municipality':
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            selected_province = Province.objects.all().get(id=province_id)
            new_municipality = Municipality()
            selected_municipality_form = MunicipalityForm(request.POST, instance=new_municipality)
            if selected_municipality_form.is_valid():
                selected_municipality_form.save()
                selected_province.municipality.add(new_municipality)
                return redirect('admin-manage-shipping', 'view_province')
    if action == 'edit_municipality':
        if request.method == 'POST':
            municipality_id = request.POST.get('municipality_id', False)
            selected_municipality = Municipality.objects.all().get(id=municipality_id)
            municipality_form = MunicipalityForm(request.POST, instance=selected_municipality)
            if municipality_form.is_valid():
                municipality_form.save()
                return redirect('admin-manage-shipping', 'view_province')
    if action == 'delete_municipality':
        if request.method == 'POST':
            municipality_id = request.POST.get('municipality_id', False)
            selected_municipality = Municipality.objects.all().get(id=municipality_id)
            selected_municipality.delete()

            return redirect('admin-manage-shipping', 'view_province')
#                                                                        #
@login_required
@permission_required('main_manager.delete_option')
def manage_coupon(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/coupon/list.html"

        try:
            all_coupons = Coupon.objects.all()
        except Coupon.DoesNotExist:
            raise Http404("No coupons")

        for c in all_coupons:
            c.clean()

        if all_coupons.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(all_coupons, 6)
        try:
            all_coupons = paginator.page(page)
        except PageNotAnInteger:
            all_coupons = paginator.page(1)
        except EmptyPage:
            all_coupons = paginator.page(paginator.num_pages)

        coupon_form = CouponForm()
        context = {
            'nav_side': 'coupon',
            'all_coupons': all_coupons,
            'paginate': paginate,
            'coupon_form': coupon_form,
        }
        return render(request, url, context)
    if action == 'add_new_coupon':
        if request.method == 'POST':
            coupon_form = CouponForm(request.POST)
            coupon_form.save()

            return redirect('admin-manage-coupon', 'main')
    if action == 'delete_coupon':
        if request.method == 'POST':
            coupon_id = request.POST.get('coupon_id', False)
            selected_coupon = Coupon.objects.all().get(id=coupon_id)
            selected_coupon.delete()

            return redirect('admin-manage-coupon', 'main')
# ---------------------------------------------------------------------- #



# ----------------------------- Customer ------------------------------- #
@login_required
def customer_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/home.html"

        context = {
            'nav_side': 'home',
        }
        return render(request, url, context)
#                                                                        #
# ---------------------------------------------------------------------- #



# ----------------------------- Seller ------------------------------- #
@login_required
def seller_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/seller/home.html"

        context = {
            'nav_side': 'home',
        }
        return render(request, url, context)
#                                                                        #
# ---------------------------------------------------------------------- #



# ----------------------------- Provider ------------------------------- #
@login_required
def provider_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/home.html"

        context = {
            'nav_side': 'home',
        }
        return render(request, url, context)
#                                                                        #
@login_required
def provider_settings(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/settings/home.html"
        store_form = StoreForm()
        update_profile_form = UpdateProfileForm()
        password_form = PasswordChangeForm(user=request.user, data=request.POST or None)

        update_profile_photo_form = UpdateProfilePhotoForm()

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        context = {
            'nav_side': 'settings',
            'store_form': store_form,
            'password_form': password_form,
            'update_profile_form': update_profile_form,
            'update_profile_photo_form': update_profile_photo_form,
            'errors': errors
        }
        return render(request, url, context)
    if action == 'edit_profile':
        if request.method == 'POST':
            update_profile_form = UpdateProfileForm(request.POST, instance=request.user)
            if update_profile_form.is_valid():
                user = update_profile_form.save()
                login(request, user)
            else:
                request.session['error_messages'] = update_profile_form.errors
            return redirect('provider-settings', 'main')
    if action == 'change_password':
        if request.method == 'POST':
            change_password_form = PasswordChangeForm(user=request.user, data=request.POST or None)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, change_password_form.user)
            else:
                request.session['error_messages'] = change_password_form.errors
            return redirect('provider-settings', 'main')
    if action == 'edit_store':
        if request.method == 'POST':
            store_form = StoreForm(request.POST, instance=request.user.store)
            if store_form.is_valid():
                store_form.save()
            else:
                request.session['error_messages'] = store_form.errors
            return redirect('provider-settings', 'main')
#                                                                        #
# ---------------------------------------------------------------------- #


