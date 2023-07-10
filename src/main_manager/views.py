from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from add_ons import functions
from django.utils import timezone
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from .models import Product, Variant, Option, Feature, Album, FlashProduct ,Description
from .forms import ProductForm, VariantForm, FeatureForm, OptionForm, FlashForm ,DescriptionForm
from main_home.forms import ProvinceForm, MunicipalityForm, CouponForm
from main_home.models import Province, Municipality, Coupon, Order
from authentication.models import User


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
    if action == 'publish_products':
        if request.method == 'POST':
            product_ids = request.POST.getlist('product_ids')
            for product_id in product_ids:
                selected_product = Variant.objects.all().get(id=product_id)
                selected_product.is_activated = True
                selected_product.save()
                selected_product.clean()
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
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/products/list.html"
        request.session['variant_id_token'] = None
        request.session['product_id_token'] = None
        all_products = Product.objects.all()
        if all_products.count():
            paginate = True
        else:
            paginate = False

        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 4)
        try:
            all_products = paginator.page(page)
        except PageNotAnInteger:
            all_products = paginator.page(1)
        except EmptyPage:
            all_products = paginator.page(paginator.num_pages)

        product_form = ProductForm()
        context = {
            'nav_side': 'products',
            'all_products': all_products,
            'paginate': paginate,
            'product_form': product_form,
        }
        return render(request, url, context)
    if action == 'add_new_product':
        if request.method == 'POST':
            new_product_form = ProductForm(request.POST)
            if new_product_form.is_valid():
                new_product_form.save()
                return redirect('manage-products', 'main')
    if action == 'delete_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product.delete()
            return redirect('manage-products', 'main')
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

            return redirect('manage-products', 'main')
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
        description_form = DescriptionForm()
        context = {
            'nav_side': 'products',
            'selected_product': selected_product,
            'selected_product_form': selected_product_form,
            'variant_form': variant_form,
            'description_form': description_form,
        }
        return render(request, url, context)
    if action == 'edit_product':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            selected_product_form = ProductForm(request.POST, instance=selected_product)
            selected_product_form.save()
            return redirect('manage-products', 'view_product')
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
            return redirect('manage-products', 'view_product')
    if action == 'delete_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant.delete()
            return redirect('manage-products', 'view_product')
    if action == 'add_description':
        if request.method == 'POST':
            product_id = request.POST.get('product_id', False)
            selected_product = Product.objects.all().get(id=product_id)
            new_description = Description(file_name=selected_product.en_title,
                                          )
            new_description.save()
            selected_description_form = DescriptionForm(request.POST, request.FILES, instance=new_description)
            selected_description_form.save()
            selected_product.description.add(new_description)
            return redirect('manage-products', 'view_product')
    if action == 'delete_description':
        if request.method == 'POST':
            description_id = request.POST.get('description_id', False)
            selected_description = Description.objects.all().get(id=description_id)
            selected_description.delete()
            return redirect('manage-products', 'view_product')
    if action == 'edit_description':
        if request.method == 'POST':
            description_id = request.POST.get('description_id', False)
            selected_description = Description.objects.all().get(id=description_id)
            selected_description_form = DescriptionForm(request.POST, request.FILES, instance=selected_description)
            selected_description_form.save()
            return redirect('manage-products', 'view_product')
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
    if action == 'edit_variant':
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id', False)
            selected_variant = Variant.objects.all().get(id=variant_id)
            selected_variant_form = VariantForm(request.POST, instance=selected_variant)
            selected_variant_form.save()

            return redirect('manage-products', 'view_variant')
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

            return redirect('manage-products', 'view_variant')
    if action == 'delete_image':
        if request.method == 'POST':
            album_id = request.POST.get('album_id', False)

            album = Album.objects.all().get(id=album_id)
            album.delete()
            return redirect('manage-products', 'view_variant')
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
            return redirect('manage-products', 'view_variant')
    if action == 'delete_feature':
        if request.method == 'POST':
            feature_id = request.POST.get('feature_id', False)

            selected_feature = Feature.objects.all().get(id=feature_id)
            selected_feature.delete()
            return redirect('manage-products', 'view_variant')
    if action == 'edit_feature':
        if request.method == 'POST':
            feature_id = request.POST.get('feature_id', False)
            selected_feature = Feature.objects.all().get(id=feature_id)

            selected_feature_form = FeatureForm(request.POST, instance=selected_feature)
            selected_feature_form.save()
            return redirect('manage-products', 'view_variant')
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
            return redirect('manage-products', 'view_variant')
    if action == 'delete_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)

            option = Option.objects.all().get(id=option_id)
            option.delete()
            return redirect('manage-products', 'view_variant')
    if action == 'edit_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)
            selected_option = Option.objects.all().get(id=option_id)

            selected_option_form = OptionForm(request.POST, request.FILES, instance=selected_option)
            selected_option_form.save()
            return redirect('manage-products', 'view_variant')
    if action == 'convert_option':
        if request.method == 'POST':
            option_id = request.POST.get('option_id', False)

            option = Option.objects.all().get(id=option_id)
            if option.has_image:
                option.has_image = False
            else:
                option.has_image = True
            option.save()
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
                return redirect('manage-flash', 'main')

def manage_orders(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    # --------------- main page ------------------- #
    if action == 'main':
        url = direction + "/management/admin/orders/list.html"
        all_orders = Order.objects.all()
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
            return redirect('manage-orders', 'main')



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
                return redirect('manage-shipping', 'main')
    if action == 'edit_province':
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            selected_province = Province.objects.all().get(id=province_id)
            province_form = ProvinceForm(request.POST, instance=selected_province)
            if province_form.is_valid():
                province_form.save()
                return redirect('manage-shipping', 'main')
    if action == 'delete_province':
        if request.method == 'POST':
            province_id = request.POST.get('province_id', False)
            selected_province = Province.objects.all().get(id=province_id)
            selected_province.delete()
            return redirect('manage-shipping', 'main')
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
                return redirect('manage-shipping', 'view_province')
    if action == 'edit_municipality':
        if request.method == 'POST':
            municipality_id = request.POST.get('municipality_id', False)
            selected_municipality = Municipality.objects.all().get(id=municipality_id)
            municipality_form = MunicipalityForm(request.POST, instance=selected_municipality)
            if municipality_form.is_valid():
                municipality_form.save()
                return redirect('manage-shipping', 'view_province')
    if action == 'delete_municipality':
        if request.method == 'POST':
            municipality_id = request.POST.get('municipality_id', False)
            selected_municipality = Municipality.objects.all().get(id=municipality_id)
            selected_municipality.delete()

            return redirect('manage-shipping', 'view_province')

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

            return redirect('manage-coupon', 'main')
    if action == 'delete_coupon':
        if request.method == 'POST':
            coupon_id = request.POST.get('coupon_id', False)
            selected_coupon = Coupon.objects.all().get(id=coupon_id)
            selected_coupon.delete()

            return redirect('manage-coupon', 'main')





