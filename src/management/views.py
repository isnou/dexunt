from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from add_ons import functions
from django.utils import timezone
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from .models import Product, Variant, Option, Feature, Album, FlashProduct, Store
from .models import Tag
from .forms import ProductForm, VariantForm, FeatureForm, OptionForm, FlashForm, StoreForm
from .forms import ENProductDescriptionForm, FRProductDescriptionForm, ARProductDescriptionForm
from home.forms import ProvinceForm, MunicipalityForm, CouponForm
from home.models import Province, Municipality, Coupon, Order, Cart
from authentication.models import User, users_filter, reset_users
from authentication.models import Transaction, transactions_select
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from authentication.forms import UpdateProfileForm, UpdatePhotoForm



# ------------------------------- Admin -------------------------------- #
@login_required
@permission_required('management.delete_option')
def admin_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
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
@permission_required('management.delete_option')
def manage_users(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    items_by_page = 20

    # -- main page -- #
    if action == 'main':
        url = direction + "/management/admin/users/list.html"
        users_list = User.objects.all().exclude(username=request.user.username)
        reset_users()

        if request.GET.get('init', None):
            request.session['users_key_word']=None
            request.session['users-page'] = None

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

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('users-page')

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
            selected_user.change_role(role)
            return redirect ('admin-manage-users', 'main')
    if action == 'add_funds':
        if request.method == 'POST':
            user_id = request.POST.get('user_id', False)
            cash = request.POST.get('cash', False)
            selected_user = User.objects.all().get(id=user_id)
            selected_user.add_funds('funds-added', cash)
            return redirect('admin-manage-users', 'main')
    # -- search partial show -- #
    if action == 'search_users':
        url = direction + "/management/admin/users/partial-list.html"
        key_word = request.GET.get('key_word', None)

        if key_word:
            request.session['users_key_word'] = key_word
        else:
            request.session['users_key_word'] = None

        users_list = User.objects.all().filter(tags__icontains=key_word).exclude(username=request.user.username)

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
@permission_required('management.delete_option')
def manage_stores(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    items_by_page = 20

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
            'stores': stores,
        }
        return render(request, url, context)
    # -- main page actions -- #
    if action == 'delete_store':
        if request.method == 'POST':
            store_id = request.POST.get('store_id', False)
            stores_page = request.POST.get('stores_page', False)
            request.session['stores-page'] = stores_page
            selected_store = Store.objects.all().get(id=store_id)
            selected_store.delete()
            return redirect ('admin-manage-stores', 'main')
    if action == 'activate_store':
        if request.method == 'POST':
            store_id = request.POST.get('store_id', False)
            stores_page = request.POST.get('stores_page', False)
            request.session['stores-page'] = stores_page
            selected_store = Store.objects.all().get(id=store_id)
            selected_store.activate()
            return redirect ('admin-manage-stores', 'main')
    if action == 'deactivate_store':
        if request.method == 'POST':
            store_id = request.POST.get('store_id', False)
            stores_page = request.POST.get('stores_page', False)
            request.session['stores-page'] = stores_page
            selected_store = Store.objects.all().get(id=store_id)
            selected_store.deactivate()
            return redirect ('admin-manage-stores', 'main')
    # -- search partial show -- #
    if action == 'search_stores':
        url = direction + "/management/admin/stores/partial-list.html"
        key_word = request.GET.get('key_word', None)
        request.session['stores_key_word'] = key_word

        stores = Store.objects.all().filter(tags__icontains=key_word)

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
            'stores': stores,
        }
        return render(request, url, context)
#                                                                        #
@login_required
@permission_required('management.delete_option')
def manage_products(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/products/list.html"
        stores = Store.objects.all()
        variants = Variant.objects.all()

        if request.GET.get('init', None):
            request.session['variants_key_word']=None
            request.session['variants-page'] = None

        if request.session.get('variants_key_word', None):
            variants = variants.filter(tags__icontains=request.session.get('variants_key_word'))
            search_key_word = request.session.get('variants_key_word')
        else:
            search_key_word = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['variants-page'] = page
        else:
            page = request.session.get('variants-page')

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        paginator = Paginator(variants, items_by_page)
        try:
            variants = paginator.page(page)
        except PageNotAnInteger:
            variants = paginator.page(1)
        except EmptyPage:
            variants = paginator.page(paginator.num_pages)

        product_form = ProductForm()
        variant_form = VariantForm()
        option_form = OptionForm()
        context = {
            'nav_side': 'products',
            'search_key_word': search_key_word,
            'variants': variants,
            'product_form': product_form,
            'variant_form': variant_form,
            'option_form': option_form,
            'errors': errors,
            'stores': stores,
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
                if new_variant_form.is_valid():
                    new_variant_form.save()
                    new_variant.product = new_product
                    new_variant.save()
                    if new_option_form.is_valid():
                        new_option_form.save()
                        new_option.variant = new_variant
                        new_option.save()
                        request.session['variant_id'] = new_variant.id
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
    if action == 'assign_provider':
        product_id = request.GET.get('product_id')
        store_id = request.GET.get('store_id')
        selected_product = Product.objects.all().get(id=product_id)
        selected_store = Store.objects.all().get(id=store_id)
        selected_store.product_set.add(selected_product)
        return redirect('admin-manage-products', 'main')
    if action == 'unassign_provider':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.store = None
            selected_product.save()
            return redirect('admin-manage-products', 'main')
    # -- search partial show -- #
    if action == 'search_products':
        url = direction + "/management/admin/products/partial-list.html"
        key_word = request.GET.get('key_word', None)
        request.session['variants_key_word'] = key_word

        variants = Variant.objects.all().filter(tags__icontains=key_word)

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['variants-page'] = page
        else:
            page = request.session.get('variants-page')

        paginator = Paginator(variants, items_by_page)
        try:
            variants = paginator.page(page)
        except PageNotAnInteger:
            variants = paginator.page(1)
        except EmptyPage:
            variants = paginator.page(paginator.num_pages)

        context = {
            'variants': variants,
        }
        return render(request, url, context)

    # --------------- selected product ------------ #
    if action == 'view_product':
        url = direction + "/management/admin/products/selected.html"

        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            request.session['product_id'] = product_id
        else:
            if request.GET.get('product_id', False):
                product_id = request.GET.get('product_id')
                request.session['product_id'] = product_id
            else:
                product_id = request.session.get('product_id')

        selected_product = Product.objects.all().get(id=product_id)

        product_form = ProductForm()
        variant_form = VariantForm()

        context = {
            'nav_side': 'products',
            'selected_product': selected_product,
            'product_form': product_form,
            'variant_form': variant_form,
        }
        return render(request, url, context)
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('admin-manage-products', 'view_product')
    if action == 'add_a_brand':
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.brand = request.POST.get('brand')
            selected_product.save()
            return redirect('admin-manage-products', 'view_product')
    if action == 'delete_brand':
        product_id = request.GET.get('product_id')
        selected_product = Product.objects.all().get(id=product_id)
        selected_product.brand = None
        selected_product.save()
        return redirect('admin-manage-products', 'view_product')
    if action == 'edit_en_description':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ENProductDescriptionForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('admin-manage-products', 'view_product')
        else:
            product_id = request.GET.get('product_id')
            selected_product = Product.objects.all().get(id=product_id)
            url = direction + "/management/admin/products/description.html"
            en_product_description_form = ENProductDescriptionForm(instance=selected_product)
            context = {
                'nav_side': 'products',
                'description': 'en',
                'selected_product': selected_product,
                'en_product_description_form': en_product_description_form,
            }
            return render(request, url, context)
    if action == 'edit_fr_description':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = FRProductDescriptionForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('admin-manage-products', 'view_product')
        else:
            product_id = request.GET.get('product_id')
            selected_product = Product.objects.all().get(id=product_id)
            url = direction + "/management/admin/products/description.html"
            fr_product_description_form = FRProductDescriptionForm(instance=selected_product)
            context = {
                'nav_side': 'products',
                'description': 'fr',
                'selected_product': selected_product,
                'fr_product_description_form': fr_product_description_form,
            }
            return render(request, url, context)
    if action == 'edit_ar_description':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ARProductDescriptionForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('admin-manage-products', 'view_product')
        else:
            product_id = request.GET.get('product_id')
            selected_product = Product.objects.all().get(id=product_id)
            url = direction + "/management/admin/products/description.html"
            ar_product_description_form = ARProductDescriptionForm(instance=selected_product)
            context = {
                'nav_side': 'products',
                'description': 'ar',
                'selected_product': selected_product,
                'ar_product_description_form': ar_product_description_form,
            }
            return render(request, url, context)
    if action == 'duplicate_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', None)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant.duplicate()
            return redirect('admin-manage-products', 'view_product')
    if action == 'delete_variant':
        variant_id = request.GET.get('variant_id')
        selected_variant = Variant.objects.all().get(id=variant_id)
        selected_product = selected_variant.product
        request.session['product_id'] = selected_product.id
        selected_variant.delete()
        return redirect('admin-manage-products', 'view_product')
    if action == 'add_tags':
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            checked_tags = request.POST.getlist('checked_tags')
            selected_product = Product.objects.all().get(id=product_id)
            for c_t in checked_tags:
                tag = Tag.objects.all().get(id=c_t)
                tag.product.add(selected_product)
            return redirect('admin-manage-products', 'view_product')
    if action == 'delete_tags':
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            checked_tags = request.POST.getlist('checked_tags')
            selected_product = Product.objects.all().get(id=product_id)
            for c_t in checked_tags:
                tag = Tag.objects.all().get(id=c_t)
                tag.product.remove(selected_product)
            return redirect('admin-manage-products', 'view_product')
    # --------------- selected variant ------------ #
    if action == 'view_variant':
        url = direction + "/management/admin/products/selected-variant.html"

        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            request.session['variant_id'] = variant_id
        else:
            if request.GET.get('variant_id', False):
                variant_id = request.GET.get('variant_id')
                request.session['variant_id'] = variant_id
            else:
                variant_id = request.session.get('variant_id')

        selected_variant = Variant.objects.all().get(id=variant_id)
        selected_variant.clean()

        variant_form = VariantForm()
        option_form = OptionForm()
        feature_form = FeatureForm()
        context = {
            'nav_side': 'products',
            'selected_variant': selected_variant,
            'variant_form': variant_form,
            'option_form': option_form,
            'feature_form': feature_form,
        }
        return render(request, url, context)
    if action == 'edit_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', None)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant_form = VariantForm(request.POST, instance=selected_variant)
            selected_variant_form.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'add_images':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', None)
            selected_variant = Variant.objects.all().get(id=variant_id)
            album = Album(file_name=selected_variant.product.en_title + '/' + selected_variant.en_spec + '/',
                          image=request.FILES.get('variant_image'),
                          )
            album.variant = selected_variant
            album.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_image':
        album_id = request.GET.get('album_id', False)
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
            selected_variant.feature_set.add(new_feature)
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_feature':
        if request.method == 'POST':
            feature_id = request.POST.get('feature_id', False)
            selected_feature = Feature.objects.all().get(id=feature_id)
            selected_feature.variant = None
            selected_feature.save()
            selected_feature.delete()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'edit_feature':
        if request.method == 'POST':
            feature_id = request.POST.get('feature_id', False)
            selected_feature = Feature.objects.all().get(id=feature_id)
            selected_feature_form = FeatureForm(request.POST, instance=selected_feature)
            selected_feature_form.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'duplicate_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            selected_option = Option.objects.all().get(id=option_id)
            selected_option.duplicate()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'edit_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            selected_option = Option.objects.all().get(id=option_id)
            selected_option_form = OptionForm(request.POST, instance=selected_option)
            selected_option_form.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'delete_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            option = Option.objects.all().get(id=option_id)
            option.delete()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'convert_option':
        if request.method == 'POST':
            selected_option = Option.objects.all().get(id=request.POST.get('option_id', False))
            selected_option.has_image = True
            selected_option.image = request.FILES.get('option_image')
            selected_option.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'deconvert_option':
        if request.method == 'POST':
            selected_option = Option.objects.all().get(id=request.POST.get('option_id', False))
            selected_option.has_image = False
            selected_option.image = None
            selected_option.save()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'activate_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            option = Option.objects.all().get(id=option_id)
            option.activate()
            return redirect('admin-manage-products', 'view_variant')
    if action == 'deactivate_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            option = Option.objects.all().get(id=option_id)
            option.deactivate()
            return redirect('admin-manage-products', 'view_variant')
#                                                                        #
@login_required
@permission_required('management.delete_option')
def manage_flash(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
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
@permission_required('management.delete_option')
def manage_orders(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/orders/list.html"
        all_orders = Order.objects.all().order_by('-updated_at')

        if all_orders.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('init', None):
            request.session['orders-page'] = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['orders-page'] = page
        else:
            page = request.session.get('orders-page')

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
            Order.objects.all().get(id=order_id).delete()
            return redirect('admin-manage-orders', 'main')
    if action == 'no_answer':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.pend(request)
        return redirect('admin-manage-orders', 'main')
    if action == 'confirmed_order':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.confirm(request)
        return redirect('admin-manage-orders', 'main')
    if action == 'collected':
        order_id = request.GET.get('order_id', False)
        product_id = request.GET.get('product_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_product = selected_order.selected_products.all().get(id=product_id)
        selected_product.collected(request)
        return redirect('admin-manage-orders', 'main')
    if action == 'controlled_quality':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.controlled(request)
        return redirect('admin-manage-orders', 'main')
    if action == 'handed_over':
        if request.method == 'POST':
            order_id = request.POST.get('order_id', False)
            selected_order = Order.objects.all().get(id=order_id)
            selected_order.handed(request)
            return redirect('admin-manage-orders', 'main')
    if action == 'paid':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.paid(request)
        return redirect('admin-manage-orders', 'main')
#                                                                        #
@login_required
@permission_required('management.delete_option')
def manage_shipping(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/shipping/provinces.html"
        provinces = Province.objects.all()

        if provinces.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('init', None):
            request.session['provinces-page'] = None
            request.session['municipalities-page'] = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['provinces-page'] = page
        else:
            page = request.session.get('provinces-page')

        paginator = Paginator(provinces, items_by_page)
        try:
            provinces = paginator.page(page)
        except PageNotAnInteger:
            provinces = paginator.page(1)
        except EmptyPage:
            provinces = paginator.page(paginator.num_pages)

        province_form = ProvinceForm()
        context = {
            'nav_side': 'shipping',
            'provinces': provinces,
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
            request.session['province_id'] = province_id
        else:
            if request.GET.get('province_id', False):
                province_id = request.GET.get('province_id')
                request.session['province_id'] = province_id
            else:
                province_id = request.session.get('province_id')

        selected_province = Province.objects.all().get(id=province_id)
        municipalities = selected_province.municipality_set.all()

        if municipalities.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('init', None):
            request.session['municipalities-page'] = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['municipalities-page'] = page
        else:
            page = request.session.get('municipalities-page')

        paginator = Paginator(municipalities, items_by_page)
        try:
            municipalities = paginator.page(page)
        except PageNotAnInteger:
            municipalities = paginator.page(1)
        except EmptyPage:
            municipalities = paginator.page(paginator.num_pages)

        selected_province_form = ProvinceForm(request.POST, instance=selected_province)
        municipality_form = MunicipalityForm()
        context = {
            'nav_side': 'shipping',
            'selected_province': selected_province,
            'municipalities': municipalities,
            'paginate': paginate,
            'selected_province_form': selected_province_form,
            'municipality_form': municipality_form,
        }
        return render(request, url, context)
    if action == 'add_municipality':
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            selected_province = Province.objects.all().get(id=province_id)
            new_municipality = Municipality(province = selected_province)
            new_municipality.save()
            selected_municipality_form = MunicipalityForm(request.POST, instance=new_municipality)
            if selected_municipality_form.is_valid():
                selected_municipality_form.save()
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
@permission_required('management.delete_option')
def manage_coupon(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')
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
#                                                                        #
@login_required
@permission_required('management.delete_option')
def manage_tags(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')

    nav_side = 'tags'
    items_by_page = 60
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/tags/list.html"

        all_tags = Tag.objects.all().order_by('-title')

        if request.GET.get('init', None):
            request.session['tags-page'] = None

        if not request.session.get('coupons_filter', None):
            request.session['coupons_filter'] = 'all'

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['tags-page'] = page
        else:
            page = request.session.get('tags-page')

        paginator = Paginator(all_tags, items_by_page)
        try:
            all_tags = paginator.page(page)
        except PageNotAnInteger:
            all_tags = paginator.page(1)
        except EmptyPage:
            all_tags = paginator.page(paginator.num_pages)

        context = {
            'nav_side': nav_side,
            'all_tags': all_tags,
        }
        return render(request, url, context)
    if action == 'add_new_tag':
        if request.method == 'POST':
            Tag(title=request.POST.get('title', False)).save()
            return redirect('admin-manage-tags', 'main')
    if action == 'delete_tag':
        tag_id = request.GET.get('tag_id', False)
        selected_tag = Tag.objects.all().get(id=tag_id)
        for p in selected_tag.product.all():
            selected_tag.product.remove(p)
        selected_tag.delete()
        return redirect('admin-manage-tags', 'main')
    if action == 'empty_tag':
        tag_id = request.GET.get('tag_id', False)
        selected_tag = Tag.objects.all().get(id=tag_id)
        for p in selected_tag.product.all():
            selected_tag.product.remove(p)
        return redirect('admin-manage-tags', 'main')
# ---------------------------------------------------------------------- #


# ------------------------------- cash --------------------------------- #
@login_required
def cash_wallet(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/cash/wallet/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = request.user.wallet.transactions.all()
        if transactions.count():
            paginate = True
        else:
            paginate = False


        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')

        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'paginate': paginate,
            'transactions': transactions,
            'provider_requests': transactions_select('provider-requests'),
            'member_requests': transactions_select('member-requests'),
            'funds_transfer': transactions_select('funds-transfer'),
            'sale_transactions': transactions_select('sale-transactions'),
            'sales_income': transactions_select('sales-income'),
            'member_transactions': transactions_select('member-transactions'),
            'members_income': transactions_select('members-income'),
            'provider_transactions': transactions_select('provider-transactions'),
            'providers_income': transactions_select('providers-income'),
        }
        return render(request, url, context)
    if action == 'confirm_transaction':
        if request.method == 'POST':
            transaction_id = request.POST.get('transaction_id', False)
            secrete_key = None
            request.user.confirm_transaction(secrete_key, transaction_id)
            return redirect('cash-wallet', 'main')
    if action == 'decline_transaction':
        if request.method == 'POST':
            transaction_id = request.POST.get('transaction_id', False)
            request.user.wallet.transactions.get(id=transaction_id).delete()
            return redirect('cash-wallet', 'main')
#                                                                        #
@login_required
def cash_sales(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/cash/sales/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = transactions_select('sale-transactions')
        if transactions.count():
            paginate = True
        else:
            paginate = False


        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')

        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'paginate': paginate,
            'transactions': transactions,
            'provider_requests': transactions_select('provider-requests'),
            'member_requests': transactions_select('member-requests'),
            'funds_transfer': transactions_select('funds-transfer'),
            'sale_transactions': transactions_select('sale-transactions'),
            'sales_income': transactions_select('sales-income'),
            'member_transactions': transactions_select('member-transactions'),
            'members_income': transactions_select('members-income'),
            'provider_transactions': transactions_select('provider-transactions'),
            'providers_income': transactions_select('providers-income'),
        }
        return render(request, url, context)
#                                                                        #
@login_required
def cash_members(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/cash/members/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = transactions_select('member-transactions')
        if transactions.count():
            paginate = True
        else:
            paginate = False


        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')

        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'paginate': paginate,
            'transactions': transactions,
            'provider_requests': transactions_select('provider-requests'),
            'member_requests': transactions_select('member-requests'),
            'funds_transfer': transactions_select('funds-transfer'),
            'sale_transactions': transactions_select('sale-transactions'),
            'sales_income': transactions_select('sales-income'),
            'member_transactions': transactions_select('member-transactions'),
            'members_income': transactions_select('members-income'),
            'provider_transactions': transactions_select('provider-transactions'),
            'providers_income': transactions_select('providers-income'),
        }
        return render(request, url, context)
#                                                                        #
@login_required
def cash_providers(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/cash/providers/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = transactions_select('provider-transactions')
        if transactions.count():
            paginate = True
        else:
            paginate = False


        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')

        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'paginate': paginate,
            'transactions': transactions,
            'provider_requests': transactions_select('provider-requests'),
            'member_requests': transactions_select('member-requests'),
            'funds_transfer': transactions_select('funds-transfer'),
            'sale_transactions': transactions_select('sale-transactions'),
            'sales_income': transactions_select('sales-income'),
            'member_transactions': transactions_select('member-transactions'),
            'members_income': transactions_select('members-income'),
            'provider_transactions': transactions_select('provider-transactions'),
            'providers_income': transactions_select('providers-income'),
        }
        return render(request, url, context)
#                                                                        #
# ---------------------------------------------------------------------- #


# ------------------------------ member -------------------------------- #
@login_required
def member_orders(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/member/orders/list.html"
        all_orders = Order.objects.all().exclude(status='created').exclude(status='completed').order_by('-id')

        if all_orders.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('init', None):
            request.session['orders-page'] = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['orders-page'] = page
        else:
            page = request.session.get('orders-page')

        paginator = Paginator(all_orders, items_by_page)
        try:
            all_orders = paginator.page(page)
        except PageNotAnInteger:
            all_orders = paginator.page(1)
        except EmptyPage:
            all_orders = paginator.page(paginator.num_pages)

        context = {
            'provider_requests': transactions_select('provider-requests'),
            'nav_side': 'orders',
            'all_orders': all_orders,
            'paginate': paginate,
        }
        return render(request, url, context)
    if action == 'no_answer':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.pend(request)
        return redirect('member-orders', 'main')
    if action == 'confirmed_order':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.confirm(request)
        return redirect('member-orders', 'main')
    if action == 'collected':
        order_id = request.GET.get('order_id', False)
        product_id = request.GET.get('product_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_product = selected_order.selected_products.all().get(id=product_id)
        selected_product.collected(request)
        return redirect('member-orders', 'main')
    if action == 'controlled_quality':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.controlled(request)
        return redirect('member-orders', 'main')
    if action == 'handed_over':
        if request.method == 'POST':
            order_id = request.POST.get('order_id', False)
            selected_order = Order.objects.all().get(id=order_id)
            selected_order.handed(request)
            return redirect('member-orders', 'main')
    if action == 'paid':
        order_id = request.GET.get('order_id', False)
        selected_order = Order.objects.all().get(id=order_id)
        selected_order.paid(request)
        return redirect('member-orders', 'main')
#                                                                        #
@login_required
def member_refunds(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/member/refunds/list.html"
        all_orders = request.user.refunds().order_by('-id')

        if all_orders.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('init', None):
            request.session['orders-page'] = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['orders-page'] = page
        else:
            page = request.session.get('orders-page')

        paginator = Paginator(all_orders, items_by_page)
        try:
            all_orders = paginator.page(page)
        except PageNotAnInteger:
            all_orders = paginator.page(1)
        except EmptyPage:
            all_orders = paginator.page(paginator.num_pages)

        context = {
            'provider_requests': transactions_select('provider-requests'),
            'nav_side': 'refund_requests',
            'all_orders': all_orders,
            'paginate': paginate,
        }
        return render(request, url, context)
#                                                                        #
@login_required
def member_profile(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/member/settings/profile.html"
        update_profile_form = UpdateProfileForm()
        password_form = PasswordChangeForm(user=request.user, data=request.POST or None)

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        context = {
            'provider_requests': transactions_select('provider-requests'),
            'nav_side': 'profile',
            'password_form': password_form,
            'update_profile_form': update_profile_form,
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
            return redirect('provider-profile', 'main')
    if action == 'change_password':
        if request.method == 'POST':
            change_password_form = PasswordChangeForm(user=request.user, data=request.POST or None)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, change_password_form.user)
            else:
                request.session['error_messages'] = change_password_form.errors
            return redirect('provider-profile', 'main')
#                                                                        #
@login_required
def member_payments(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/member/payments/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = transactions_select('provider-requests')

        if transactions.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')

        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'payment_request',
            'transactions': transactions,
            'paginate': paginate,
        }
        return render(request, url, context)
    if action == 'confirm':
        if request.method == 'POST':
            nav_side = request.POST.get('nav_side', False)
            transaction_id = request.POST.get('transaction_id', False)
            secrete_key = request.POST.get('secrete_key', False)
            request.user.confirm_transaction(secrete_key, transaction_id)
            if nav_side == 'orders':
                return redirect('member-orders', 'main')
            if nav_side == 'profile':
                return redirect('member-profile', 'main')
            if nav_side == 'my_wallet':
                return redirect('member-wallet', 'main')
            if nav_side == 'payment_request':
                return redirect('member-payments', 'main')
    if action == 'decline_transaction':
        if request.method == 'POST':
            transaction_id = request.POST.get('transaction_id', False)
            request.user.wallet.transactions.get(id=transaction_id).delete()
            return redirect('member-home', 'main')
#                                                                        #
@login_required
def member_wallet(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/member/wallet/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = request.user.wallet.transactions.all()

        if transactions.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')


        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'provider_requests': transactions_select('provider-requests'),
            'nav_side': 'my_wallet',
            'transactions': transactions,
            'paginate': paginate,
        }
        return render(request, url, context)
    if action == 'request_funds':
        if request.method == 'POST':
            nav_side = request.POST.get('nav_side', False)
            amount = request.POST.get('amount', False)
            request.user.request_transaction('member-payment-request', amount, False)
            if nav_side == 'orders':
                return redirect('member-orders', 'main')
            if nav_side == 'profile':
                return redirect('member-profile', 'main')
            if nav_side == 'my_wallet':
                return redirect('member-wallet', 'main')
            if nav_side == 'payment_request':
                return redirect('member-payments', 'main')
    if action == 'funds_transfer':
        if request.method == 'POST':
            amount = request.POST.get('amount', False)
            request.user.add_funds('member-funds-transfer', amount)
            return redirect('member-wallet', 'main')
# ---------------------------------------------------------------------- #


# ----------------------------- Customer ------------------------------- #
@login_required
def customer_orders(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/orders/list.html"

        context = {
            'source_page': 'customer-orders',
            'nav_side': 'orders',
        }
        return render(request, url, context)
#                                                                        #
@login_required
def customer_discount(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/discount/list.html"

        context = {
            'nav_side': 'discount',
        }
        return render(request, url, context)
#                                                                        #
@login_required
def customer_transactions(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/transactions/list.html"

        context = {
            'nav_side': 'transactions',
        }
        return render(request, url, context)
    if action == 'complete_order':
        if request.method == 'POST':
            selected_order = request.user.all_orders.all().get(id=request.POST.get('order_id', False))
            selected_order.completed(request)
            return redirect('customer-transactions', 'main')
    if action == 'refund_request':
        if request.method == 'POST':
            selected_order = request.user.all_orders.all().get(id=request.POST.get('order_id', False))
            selected_order.refund_request(request)
            return redirect('customer-transactions', 'main')
#                                                                        #
@login_required
def customer_wallet(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/wallet/home.html"

        context = {
            'nav_side': 'my-wallet',
        }
        return render(request, url, context)
#                                                                        #
@login_required
def customer_address(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/address/edit.html"
        provinces = Province.objects.all()

        context = {
            'source_page': 'customer-address',
            'nav_side': 'address',
            'provinces': provinces,
        }
        return render(request, url, context)
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
    if action == 'delete_address':
        address_id = request.GET.get('address_id')
        delivery_address = request.user.delivery_addresses.all().get(id=address_id)
        delivery_address.delete()
        return redirect('customer-address', 'main')
    if action == 'set_address_as_default':
        request.user.set_address_as_default(request)
        return redirect('customer-address', 'main')
    if action == 'edit_address':
        request.user.edit_address(request)
        return redirect('customer-address', 'main')
#                                                                        #
@login_required
def customer_settings(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/customer/settings/profile.html"
        update_profile_form = UpdateProfileForm()
        password_form = PasswordChangeForm(user=request.user, data=request.POST or None)

        context = {
            'nav_side': 'settings',
            'update_profile_form': update_profile_form,
            'password_form': password_form,
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
            return redirect('customer-settings', 'main')
    if action == 'edit_password':
        if request.method == 'POST':
            change_password_form = PasswordChangeForm(user=request.user, data=request.POST or None)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, change_password_form.user)
            else:
                request.session['error_messages'] = change_password_form.errors
            return redirect('customer-settings', 'main')
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
def provider_profile(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/settings/profile.html"
        update_profile_form = UpdateProfileForm()
        password_form = PasswordChangeForm(user=request.user, data=request.POST or None)

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        context = {
            'nav_side': 'profile',
            'password_form': password_form,
            'update_profile_form': update_profile_form,
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
            return redirect('provider-profile', 'main')
    if action == 'change_password':
        if request.method == 'POST':
            change_password_form = PasswordChangeForm(user=request.user, data=request.POST or None)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, change_password_form.user)
            else:
                request.session['error_messages'] = change_password_form.errors
            return redirect('provider-profile', 'main')
#                                                                        #
@login_required
def provider_store(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/settings/store.html"
        store_form = StoreForm()
        update_photo_form = UpdatePhotoForm()

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        context = {
            'nav_side': 'store',
            'store_form': store_form,
            'update_photo_form': update_photo_form,
            'errors': errors
        }
        return render(request, url, context)
    if action == 'edit_store':
        if request.method == 'POST':
            store_form = StoreForm(request.POST, instance=request.user.store)
            if store_form.is_valid():
                store_form.save()
            else:
                request.session['error_messages'] = store_form.errors
            return redirect('provider-store', 'main')
    if action == 'edit_logo':
        if request.method == 'POST':
            request.user.save()
            update_photo_form = UpdatePhotoForm(request.POST, request.FILES, instance=request.user)
            if update_photo_form.is_valid():
                update_photo_form.save()
            else:
                request.session['error_messages'] = update_photo_form.errors
            return redirect('provider-store', 'main')
#                                                                        #
@login_required
def provider_products(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/products/list.html"

        variants = request.user.store.all_variants()

        if request.GET.get('init', None):
            request.session['variants_key_word']=None
            request.session['variants-page'] = None

        if request.session.get('variants_key_word', None):
            variants = variants.filter(tags__icontains=request.session.get('variants_key_word'))
            search_key_word = request.session.get('variants_key_word')
        else:
            search_key_word = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['variants-page'] = page
        else:
            page = request.session.get('variants-page')

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        paginator = Paginator(variants, items_by_page)
        try:
            variants = paginator.page(page)
        except PageNotAnInteger:
            variants = paginator.page(1)
        except EmptyPage:
            variants = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'my_products',
            'search_key_word': search_key_word,
            'variants': variants,
            'errors': errors,
        }
        return render(request, url, context)
    # -- search partial show -- #
    if action == 'search_products':
        url = direction + "/management/provider/products/partial-list.html"
        key_word = request.GET.get('key_word', None)
        request.session['variants_key_word'] = key_word

        variant_ids = []
        for p in request.user.store.product_set.all():
            for v in p.variant_set.all():
                variant_ids.append(v.id)
        variants = Variant.objects.filter(id__in=variant_ids)

        variants = variants.filter(tags__icontains=key_word)

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['variants-page'] = page
        else:
            page = request.session.get('variants-page')

        paginator = Paginator(variants, items_by_page)
        try:
            variants = paginator.page(page)
        except PageNotAnInteger:
            variants = paginator.page(1)
        except EmptyPage:
            variants = paginator.page(paginator.num_pages)

        context = {
            'variants': variants,
        }
        return render(request, url, context)
    if action == 'edit_price':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            price = int(request.POST.get('price', False))
            selected_option = Option.objects.all().get(id=option_id)
            selected_option.cost = price
            selected_option.is_activated = False
            selected_option.save()
            return redirect('provider-products', 'main')
    if action == 'add_quantity':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            quantity = int(request.POST.get('quantity', False))
            selected_option = Option.objects.all().get(id=option_id)
            selected_option.quantity += quantity
            selected_option.save()
            return redirect('provider-products', 'main')
    if action == 'remove_quantity':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            quantity = int(request.POST.get('quantity', False))
            selected_option = Option.objects.all().get(id=option_id)
            if quantity <= selected_option.quantity:
                selected_option.quantity -= quantity
                selected_option.save()
            return redirect('provider-products', 'main')
    if action == 'deactivate':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            selected_option = Option.objects.all().get(id=option_id)
            selected_option.deactivate()
            return redirect('provider-products', 'main')
#                                                                        #
@login_required
def provider_sales(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/sales/list.html"

        orders = request.user.store.orders.all().order_by('-id')

        if request.GET.get('init', None):
            request.session['orders-page'] = None

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
            request.session['orders-page'] = page
        else:
            page = request.session.get('orders-page')

        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None

        paginator = Paginator(orders, items_by_page)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'my_sales',
            'orders': orders,
            'errors': errors,
        }
        return render(request, url, context)
    if action == 'validate_order':
        order_id = request.GET.get('order_id', False)
        selected_order = request.user.store.orders.all().get(id=order_id)
        selected_order.process()
        return redirect('provider-sales', 'main')
#                                                                        #
@login_required
def provider_wallet(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    items_by_page = 20

    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/provider/wallet/list.html"
        if request.GET.get('init', None):
            request.session['transactions-page'] = None

        transactions = request.user.wallet.transactions.all()

        if transactions.count():
            paginate = True
        else:
            paginate = False

        if request.GET.get('page', None):
            page = request.GET.get('page', 1)
        else:
            page = request.session.get('transactions-page')


        paginator = Paginator(transactions, items_by_page)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context = {
            'nav_side': 'my_wallet',
            'transactions': transactions,
            'paginate': paginate,
        }
        return render(request, url, context)
    if action == 'request_payment':
        if request.method == 'POST':
            amount = request.POST.get('amount', False)
            request.user.request_transaction('provider-payment-request', amount, True)
            return redirect('provider-wallet', 'main')
# ---------------------------------------------------------------------- #


