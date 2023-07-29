from django.db import models
from add_ons import functions
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# ------------------------------- Orders ------------------------------- #
class SelectedProduct(models.Model):
    # ----- Technical ----- #
    lack_of_quantity = models.BooleanField(default=False)
    # ----- #
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered_at = models.DateTimeField(blank=True, null=True) # -- a new confirmed order
    is_prepared_at = models.DateTimeField(blank=True, null=True) # -- order prepared by the provider
    is_paid_at = models.DateTimeField(blank=True, null=True)
    is_refunded_at = models.DateTimeField(blank=True, null=True)
    # ----- relations ----- #
    option = models.ForeignKey(
        'management.Option', on_delete=models.CASCADE, related_name='selected_products', null=True)
    cart = models.ForeignKey(
        'home.Cart', on_delete=models.CASCADE, related_name='selected_products', null=True)
    order = models.ForeignKey(
        'home.Order', on_delete=models.CASCADE, related_name='selected_products', null=True)
    # ----- content ----- #
    quantity = models.IntegerField(default=1)
    retained_points = models.IntegerField(default=0)
    retained_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    retained_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
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
    def points(self):
        return self.option.points * self.quantity
    def en_title(self):
        return self.option.variant.product.en_title
    def en_detail(self):
        return self.option.variant.en_spec + ' ' + self.option.en_value
    def fr_title(self):
        return self.option.variant.product.fr_title
    def fr_detail(self):
        return self.option.variant.fr_spec + ' ' + self.option.fr_value
    def ar_title(self):
        return self.option.variant.product.ar_title
    def ar_detail(self):
        return self.option.variant.ar_spec + ' ' + self.option.ar_value
    def status(self):
        status = 'created'
        if self.is_ordered_at:
            status = 'pending'
        if self.is_prepared_at:
            status = 'prepared'
        if self.is_paid_at:
            status = 'paid'
        if self.is_refunded_at:
            status = 'refunded'
        return  status
    def quantity_control(self):
        if self.quantity > self.option.quantity:
            self.lack_of_quantity = True
        super().save()
    def place_order(self):
        self.quantity_control()
        self.cart.coupon = None
        self.cart.save()
        self.cart = None
        self.retained_points = self.points()
        self.retained_price = self.price()
        self.retained_total_price = self.total_price()
        super().save()
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
    def check_availability(self):
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
        coupon.check_availability()
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
    # related to many selected_products #
    coupon = models.ForeignKey(
        'home.Coupon', on_delete=models.CASCADE, null=True)
    # ----- functions ----- #
    def price(self):
        price = 0
        for p in self.selected_products.all():
            price += p.total_price()
        return price
    def total_price(self):
        total_price = self.price()
        if self.coupon:
            self.coupon.check_availability()
            if self.coupon.is_active:
                if self.coupon.is_subtractive:
                    total_price = total_price - self.coupon.value
                else:
                    total_price = total_price - ((total_price * self.coupon.value) / 100)
        return total_price
    def points(self):
        points = 0
        for p in self.selected_products.all():
            points += p.points()
        return points
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = functions.serial_number_generator(20).upper()
        super().save()
    def add_product(self, option):
        if self.selected_products.all().filter(option_id=option.id).exists():
            selected_product = self.selected_products.all().get(option_id=option.id)
            selected_product.quantity += 1
            selected_product.save()
        else:
            selected_product = SelectedProduct(option=option)
            selected_product.cart = self
            selected_product.save()
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
    ref = models.CharField(max_length=6, unique=True, null=True)
    # ----- #
    number_of_calls = models.IntegerField(default=0)

    is_empty = models.BooleanField(default=True) # -- new order
    created_at = models.DateTimeField(auto_now_add=True)
    placed_at = models.DateTimeField(blank=True, null=True) # -- waiting for confirmation
    pending_since = models.DateTimeField(blank=True, null=True) # -- no answers
    cancelled_at = models.DateTimeField(blank=True, null=True) # -- by the customer or after multiple calls
    confirmed_at = models.DateTimeField(blank=True, null=True) # -- confirmed order and waiting for providers
    being_processed_since = models.DateTimeField(blank=True, null=True) # -- all products prepared by different providers
    quality_control_since = models.DateTimeField(blank=True, null=True) # -- check before expedition
    on_delivery_since = models.DateTimeField(blank=True, null=True) # -- products shipped
    paid_at = models.DateTimeField(blank=True, null=True) # -- received and paid by the client
    refund_request_at = models.DateTimeField(blank=True, null=True)
    refunded_at = models.DateTimeField(blank=True, null=True)
    # ----- relations ----- #
    # related to many selected_products #
    coupon = models.ForeignKey(
        'home.Coupon', on_delete=models.CASCADE, null=True)
    municipality = models.ForeignKey(
        'home.Municipality', on_delete=models.CASCADE, null=True)
    # ----- #
    placed_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='placed_orders', blank=True, null=True)
    cancelled_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='cancelled_orders', blank=True, null=True)
    confirmed_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='confirmed_orders', blank=True, null=True)
    quality_control_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='orders_under_quality_control', blank=True, null=True)
    on_delivery_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='orders_on_delivery', blank=True, null=True)
    paid_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='paid_products', blank=True, null=True)
    refunded_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='refunded_orders', blank=True, null=True)
    # ----- content ----- #
    client_name = models.CharField(max_length=300, blank=True, null=True)
    client_phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    retained_points = models.IntegerField(default=0)
    retained_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    retained_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # --------------------------------- order info ---------------------------------------------
    delivery_type = models.CharField(max_length=100, default='HOME') # -- delivery_types :  HOME - DESK
    # ----- functions ----- #
    def delivery_price(self):
        delivery_q = 0
        if self.selected_products.all().count():
            for p in self.selected_products.all():
                delivery_q += p.option.delivery_quotient
            delivery_q = float(delivery_q / self.selected_products.all().count())

            if self.municipality:
                if self.delivery_type == 'HOME':
                    return int(float(self.municipality.home_delivery_price) * delivery_q / 100)
                if self.delivery_type == 'DESK':
                    return int(float(self.municipality.desk_delivery_price) * delivery_q / 100)
        super().save()
    def price(self):
        price = 0
        for p in self.selected_products.all():
            price += p.total_price()
        return price
    def total_price(self):
        if self.delivery_price():
            total_price = self.price() + self.delivery_price()
        else:
            total_price = self.price()
        if self.coupon:
            self.coupon.check_availability()
            if self.coupon.is_active:
                if self.coupon.is_subtractive:
                    total_price = total_price - self.coupon.value
                else:
                    total_price = total_price - ((total_price * self.coupon.value) / 100)
        return total_price
    def points(self):
        points = 0
        for p in self.selected_products.all():
            points += p.points()
        return points
    def status(self):
        status = 'created'
        if self.placed_at:
            status = 'confirmation'
        if self.pending_since:
            status = 'pending'
        if self.cancelled_at:
            status = 'cancelled'
        if self.confirmed_at:
            status = 'confirmed'
        if self.being_processed_since:
            status = 'processed'
        if self.quality_control_since:
            status = 'quality'
        if self.on_delivery_since:
            status = 'delivery'
        if self.paid_at:
            status = 'paid'
        if self.refund_request_at:
            status = 'dispute'
        if self.refunded_at:
            status = 'refund'
        return  status
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = functions.serial_number_generator(6).upper()
        super().save()
    def place_order(self, request):
        for p in self.selected_products.all():
            p.place_order()
        self.is_empty = False
        self.placed_at = timezone.now()
        self.retained_points = self.points()
        self.retained_price = self.price()
        self.retained_total_price = self.total_price()
        if not request.user.is_authenticated:
            request.session['order_ref'] = None
            request.session['cart_ref'] = None
        super().save()
#                                                                        #
def get_order(request):
    selected_cart = get_cart(request)
    coupon = selected_cart.coupon
    if not request.user.is_authenticated:
        if not request.session.get('order_ref', None):
            selected_order = Order(coupon=coupon)
            selected_order.save()
            request.session['order_ref'] = selected_order.ref
        else:
            if Order.objects.all().filter(ref=request.session.get('order_ref')).exists():
                selected_order = Order.objects.all().get(ref=request.session.get('order_ref'))
                selected_order.coupon=coupon
                selected_order.save()
            else:
                selected_order = Order(coupon=coupon)
                selected_order.save()
                request.session['order_ref'] = selected_order.ref
    else:
        if request.user.placed_orders.all().filter(is_empty=True).exists():
            selected_order = request.user.placed_orders.all().get(is_empty=True)
            selected_order.coupon = coupon
            selected_order.save()
        else:
            selected_order = Order(coupon=coupon)
            selected_order.save()
            request.user.placed_orders.add(selected_order)

    for p in selected_cart.selected_products.all():
        p.order = selected_order
        p.save()

    return selected_order
# ---------------------------------------------------------------------- #


# ------------------------------ Shipping ------------------------------ #
class Municipality(models.Model):
    # ----- content ----- #
    en_name = models.CharField(max_length=200, blank=True, null=True)
    fr_name = models.CharField(max_length=200, blank=True, null=True)
    ar_name = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    fr_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    ar_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    home_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    desk_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- relations ----- #
    # related to many order #
    province = models.ForeignKey(
        'home.Province', on_delete=models.CASCADE, null=True)
    # ----- functions ----- #
    class Meta:
        verbose_name_plural = "Municipalities"
#                                                                        #
class Province(models.Model):
    # ----- content ----- #
    en_name = models.CharField(max_length=200, blank=True, null=True)
    fr_name = models.CharField(max_length=200, blank=True, null=True)
    ar_name = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    fr_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    ar_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    home_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    desk_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- relations ----- #
    # related to many municipalities #
# ---------------------------------------------------------------------- #


