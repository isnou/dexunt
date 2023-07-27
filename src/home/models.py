from django.db import models
from add_ons import functions
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# ------------------------------- Orders ------------------------------- #
class SelectedProduct(models.Model):
    # ----- Technical ----- #
    created_at = models.DateTimeField(auto_now_add=True)
    lack_of_quantity = models.BooleanField(default=False)
    # ----- relations ----- #
    option = models.ForeignKey(
        'management.Option', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    quantity = models.IntegerField(default=1)
    # ----- functions ----- #
    def image(self):
        if self.option.has_image:
            return self.option.image
        else:
            return self.option.variant.album_set.all().first().image
    def price(self):
        if self.option.discount:
            return self.option.discount
        else:
            return self.option.price
    def total_price(self):
        if self.option.discount:
            return self.option.discount * self.quantity
        else:
            return self.option.price * self.quantity
    def en_tite(self):
        return self.option.variant.product.en_title
    def en_detail(self):
        return self.option.variant.en_spec + ' ' + self.option.en_value
    def fr_tite(self):
        return self.option.variant.product.fr_title
    def fr_detail(self):
        return self.option.variant.fr_spec + ' ' + self.option.fr_value
    def ar_tite(self):
        return self.option.variant.product.ar_title
    def ar_detail(self):
        return self.option.variant.ar_spec + ' ' + self.option.ar_value
#                                                                        #
class Coupon(models.Model):
    # ----- Technical ----- #
    is_subtractive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # ----- content ----- #
    quantity = models.IntegerField(default=1)
    code = models.CharField(max_length=20, unique=True, null=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if self.is_subtractive:
            if self.value < 0:
                self.value = 0
        else:
            if self.value < 0:
                self.value = 0
            elif self.value > 100:
                self.value = 100
        super().save()
    def check(self):
        if self.valid_until <= timezone.now():
            self.is_active = False
        if self.quantity == 0:
            self.is_active = False
        super().save()
#                                                                        #
def apply_coupon(request, selected_cart):
    coupon_code = request.POST.get('coupon_code', False)
    if Coupon.objects.all().filter(code=coupon_code).exists():
        coupon = Coupon.objects.all().get(code=coupon_code)
        coupon.check()
        if coupon.is_active:
            request.session['coupon_message'] = 'success'
            selected_cart.coupon = coupon
            selected_cart.save()
        else:
            request.session['coupon_message'] = 'expired'
    else:
        request.session['coupon_message'] = 'wrong'
#                                                                        #
class Cart(models.Model):
    # ----- Technical ----- #
    ref = models.CharField(max_length=20, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ----- relations ----- #
    coupon = models.ForeignKey(
        'home.Coupon', on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(SelectedProduct, blank=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = functions.serial_number_generator(20).upper()
        super().save()
    def add_product(self, option):
        selected_product = None
        if self.product.all().filter(option_id=option.id).exists():
            selected_product = self.product.all().get(option_id=option.id)
            selected_product.quantity += 1
            selected_product.save()

        if not selected_product:
            selected_product = SelectedProduct(option=option)
            selected_product.save()
            self.product.add(selected_product)
    def price(self):
        price = 0
        for p in self.product.all():
            price += p.total_price()
        return price
    def total_price(self):
        total_price = self.price()
        if self.coupon:
            self.coupon.check()
            if self.coupon.is_active:
                if self.coupon.is_subtractive:
                    total_price = total_price - self.coupon.value
                else:
                    total_price = total_price - ((total_price * self.coupon.value) / 100)
        return total_price
#                                                                        #
def get_cart(request):
    if not request.user.is_authenticated:
        if not request.session.get('cart_ref', None):
            selected_cart = Cart()
            selected_cart.save()
            request.session['cart_ref'] = selected_cart.ref
        else:
            ref = request.session.get('cart_ref')
            if Cart.objects.all().filter(ref=ref).exists():
                selected_cart = Cart.objects.all().get(ref=ref)
            else:
                selected_cart = Cart()
                selected_cart.save()
                request.session['cart_ref'] = selected_cart.ref
    else:
        selected_cart = request.user.cart
    return selected_cart
#                                                                        #
class Order(models.Model):
    # ----- Technical ----- #
    is_regular = models.BooleanField(default=True)
    is_flash = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    my_qr = models.BooleanField(default=False)
    gift_card = models.BooleanField(default=False)
    # ----- #
    cart_ref = models.CharField(max_length=20, blank=True, null=True)
    ref = models.CharField(max_length=6, unique=True, null=True)
    quantity_issue = models.BooleanField(default=False)
    # ----- #
    is_incomplete = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- #
    is_fulfilled = models.BooleanField(default=False)
    fulfilled_at = models.DateTimeField(blank=True, null=True)
    # ----- #
    is_pending = models.BooleanField(default=False)
    pended_at = models.DateTimeField(blank=True, null=True)
    pended_by = models.CharField(max_length=24, blank=True, null=True) # -- by a member
    # ----- #
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=24, blank=True, null=True) # -- by a member
    # ----- #
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmation_by = models.CharField(max_length=24, blank=True, null=True) # -- by a member
    # ----- #
    is_processing = models.BooleanField(default=False)
    processing_at = models.DateTimeField(blank=True, null=True)
    processing_by = models.CharField(max_length=24, blank=True, null=True) # -- by the provider
    # ----- #
    is_quality_checking = models.BooleanField(default=False)
    quality_checking_at = models.DateTimeField(blank=True, null=True)
    quality_checking_by = models.CharField(max_length=24, blank=True, null=True)  # -- by a member
    # ----- #
    is_given_for_delivery = models.BooleanField(default=False)
    given_for_delivery_at = models.DateTimeField(blank=True, null=True)
    given_for_delivery_by = models.CharField(max_length=24, blank=True, null=True)  # -- by a member
    # ----- #
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    paid_by = models.CharField(max_length=24, blank=True, null=True)  # -- by a member
    # ----- #
    refund_request = models.BooleanField(default=False)
    refund_request_at = models.DateTimeField(blank=True, null=True)
    refund_request_by = models.CharField(max_length=24, blank=True, null=True)  # -- by a member
    # ----- #
    is_refunded = models.BooleanField(default=False)
    refunded_at = models.DateTimeField(blank=True, null=True)
    refunded_by = models.CharField(max_length=24, blank=True, null=True)  # -- by a member
    # ----- relations ----- #
    product = models.ManyToManyField(SelectedProduct, blank=True)
    # ----- content ----- #
    client_name = models.CharField(max_length=300, blank=True, null=True)
    client_phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    # --------------------------------- order info ---------------------------------------------
    points = models.IntegerField(default=0)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    coupon_value = models.IntegerField(default=0, null=True)
    has_subtractive_coupon = models.BooleanField(default=True)

    delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    delivery_type = models.CharField(max_length=100, default='HOME') # -- delivery_types :  HOME - DESK

    sub_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = functions.serial_number_generator(6).upper()
        super().save()
    def update_prices(self):
        if not self.coupon_value:
            if self.delivery_price:
                self.total_price = self.sub_total_price + self.delivery_price
            else:
                self.total_price = self.sub_total_price
        else:
            if self.delivery_price:
                if self.has_subtractive_coupon:
                    self.total_price = self.sub_total_price - self.coupon_value + self.delivery_price
                else:
                    self.total_price = self.sub_total_price - (( self.sub_total_price * self.coupon_value ) / 100) + self.delivery_price
            else:
                if self.has_subtractive_coupon:
                    self.total_price = self.sub_total_price - self.coupon_value
                else:
                    self.total_price = self.sub_total_price - (( self.sub_total_price * self.coupon_value ) / 100)
        super().save()
    def delete_products(self):
        for product in self.product.all():
            product.delete()
        super().save()
#                                                                        #
def get_order(request, selected_cart):
    if not request.user.is_authenticated:
        if not request.session.get('order_ref', None):
            selected_order = Order(cart_ref=selected_cart.ref,)
            selected_order.save()
            request.session['order_ref'] = selected_order.ref
        else:
            ref = request.session.get('order_ref')
            if Order.objects.all().filter(ref=ref).exists():
                selected_order = Order.objects.all().get(ref=ref)
            else:
                selected_order = Order(cart_ref=selected_cart.ref,)
                selected_order.save()
                request.session['order_ref'] = selected_order.ref
    else:
        if request.user.order.all().filter(is_incomplete=True).exists():
            selected_order = Order.objects.all().get(is_incomplete=True)
        else:
            selected_order = Order(cart_ref=selected_cart.ref)
            selected_order.save()
            request.user.order,add(selected_order)

    new_points = 0
    for p in selected_cart.product.all():
        selected_order.product.add(p)
        new_points += (p.points * p.quantity)

    selected_order.coupon_code = selected_cart.coupon_code
    selected_order.has_subtractive_coupon = selected_cart.has_subtractive_coupon
    selected_order.coupon_value = selected_cart.coupon_value
    selected_order.points = new_points
    selected_order.sub_total_price = selected_cart.sub_total_price

    selected_order.update_prices()

    return selected_order
#                                                                        #
def place_order(request, selected_cart, selected_order):
    selected_order.is_incomplete = False
    selected_order.is_fulfilled = True
    selected_order.fulfilled_at = timezone.now()
    selected_order.update_prices()
    selected_cart.delete()

    request.session['municipality_id_token'] = None
    request.session['order_ref'] = None
    request.session['cart_ref'] = None
# ---------------------------------------------------------------------- #


# ------------------------------ Shipping ------------------------------ #
class Municipality(models.Model):
    # ----- content ----- #
    en_name = models.CharField(max_length=200, blank=True, null=True)
    fr_name = models.CharField(max_length=200, blank=True, null=True)
    ar_name = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_home_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    fr_home_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    ar_home_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    home_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- #
    en_desk_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    fr_desk_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    ar_desk_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    desk_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    class Meta:
        verbose_name_plural = "Municipalities"
#                                                                        #
class Province(models.Model):
    # ----- content ----- #
    en_name = models.CharField(max_length=200, blank=True, null=True)
    fr_name = models.CharField(max_length=200, blank=True, null=True)
    ar_name = models.CharField(max_length=200, blank=True, null=True)
    # ----- functions ----- #
    municipality = models.ManyToManyField(Municipality, blank=True)
# ---------------------------------------------------------------------- #


