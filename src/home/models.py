from django.db import models
from add_ons import functions
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# ------------------------------- Orders ------------------------------- #
class Log(models.Model):
    # ----- Technical ----- #
    content = models.CharField(max_length=500, default='created', null=True)
    at = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    user = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='log', blank=True, null=True)
    store = models.ForeignKey(
        'management.Store', on_delete=models.CASCADE, related_name='log', blank=True, null=True)
    order = models.ForeignKey(
        'home.Order', on_delete=models.CASCADE, related_name='log', null=True)
    selected_product = models.ForeignKey(
        'home.SelectedProduct', on_delete=models.CASCADE, related_name='log', null=True)
#                                                                        #
class SelectedProduct(models.Model):
    # ----- Technical ----- #
    lack_of_quantity = models.BooleanField(default=False)
    # ----- #
    status = models.CharField(max_length=50, default='created', null=True)
    # ----- relations ----- #
    store = models.ForeignKey(
        'management.Store', on_delete=models.CASCADE, related_name='orders', null=True)
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
    def quantity_control(self):
        if self.quantity > self.option.quantity:
            self.lack_of_quantity = True
        else:
            self.lack_of_quantity = False
        super().save()
    def new_log(self):
        new_log = Log(content=self.status,
                      store=self.store,
                      selected_product=self)
        new_log.save()
    def place_order(self):
        self.quantity_control()
        self.cart = None
        self.retained_points = self.points()
        self.retained_price = self.price()
        self.retained_total_price = self.total_price()
        super().save()
        self.new_log()
    def confirm(self):
        self.status = 'confirmed'
        self.store = self.option.variant.product.store
        super().save()
        self.new_log()
    def process(self):
        self.quantity_control()
        if not self.lack_of_quantity:
            self.option.quantity -= self.quantity
            self.option.save()
            self.status = 'processed'
            self.store = self.option.variant.product.store
            super().save()
            self.new_log()
    def collected(self, request):
        self.status = 'collected'
        self.store = self.option.variant.product.store
        super().save()
        new_log = Log(content=self.status,
                      store=self.store,
                      user=request.user,
                      selected_product=self)
        new_log.save()
        processed = True
        for p in self.order.selected_products.all():
            if not p.status == 'collected':
                processed = False
        if processed:
            self.order.process()
    # ----- variables ----- #
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
        'home.Coupon', on_delete=models.CASCADE, blank=True, null=True)
    # ----- functions ----- #
    def __str__(self):
        return self.ref
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = 'CART-' + functions.serial_number_generator(15).upper()
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
    # ----- variables ----- #
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
    updated_at = models.DateTimeField(auto_now=True)
    is_regular = models.BooleanField(default=True)
    is_flash = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    my_qr = models.BooleanField(default=False)
    gift_card = models.BooleanField(default=False)
    # ----- #
    cash_on_delivery = models.BooleanField(default=True)
    # ----- #
    ref = models.CharField(max_length=6, unique=True, null=True)
    secret_key = models.CharField(max_length=6, unique=True, null=True)
    delivery_code = models.CharField(max_length=30, blank=True, null=True)
    # ----- #
    status = models.CharField(max_length=50, default='created', null=True)
    # ----- relations ----- #
    # related to many selected_products #
    coupon = models.ForeignKey(
        'home.Coupon', blank=True, on_delete=models.CASCADE, null=True)
    municipality = models.ForeignKey(
        'home.Municipality', blank=True, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='all_orders', blank=True, null=True)
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
    def save(self, *args, **kwargs):
        if not self.secret_key:
            self.secret_key = functions.serial_number_generator(6)
        super().save()
        if not self.ref:
            self.ref = str(self.id+1).zfill(6)
        super().save()
    def new_log(self, request):
        new_log = Log(content=self.status,
                      order=self)
        if request.user.is_authenticated:
            new_log.user=request.user
        new_log.save()
    def placing(self, request):
        if request.user.is_authenticated:
            request.user.cart.coupon = None
            request.user.cart.save()
        else:
            request.session['order_ref'] = None
            request.session['cart_ref'] = None
        for p in self.selected_products.all():
            p.place_order()
        self.retained_points = self.points()
        self.retained_price = self.price()
        self.retained_total_price = self.total_price()
        self.status = 'placed'
        super().save()
        self.new_log(request)
    def confirm(self, request):
        for p in self.selected_products.all():
            p.confirm()
        self.status = 'confirmed'
        super().save()
        self.new_log(request)
    def cancel(self, request):
        self.status = 'cancelled'
        super().save()
        self.new_log(request)
    def pend(self, request):
        new_log = Log(content='pend',
                      user=request.user,
                      order=self)
        new_log.save()
    def process(self):
        self.status = 'processed'
        super().save()
        new_log = Log(content=self.status,
                      order=self)
        new_log.save()
    def controlled(self, request):
        self.status = 'controlled'
        super().save()
        self.new_log(request)
    def handed(self, request):
        delivery_code = request.POST.get('delivery_code', False)
        self.delivery_code = delivery_code
        self.status = 'handed'
        super().save()
        self.new_log(request)
    def paid(self, request):
        self.paid_by = request.user
        self.paid_at = timezone.now()
    def refund(self, request):
        self.refunded_by = request.user
        self.refunded_at = timezone.now()
        super().save()
    # ----- variables ----- #
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
    def progress(self):
        if self.status == 'created':
            return 10
        if self.status == 'placed':
            return 20
        if self.status == 'confirmed':
            return 30
        if self.status == 'processed':
            return 40
        if self.status == 'controlled':
            return 50
        if self.status == 'handed':
            return 60
        if self.status == 'paid':
            return 100
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
        if request.user.all_orders.all().filter(status='created').exists():
            selected_order = request.user.all_orders.all().get(status='created')
            selected_order.coupon = coupon
            selected_order.save()
        else:
            selected_order = Order(coupon=coupon,
                                   client=request.user)
            selected_order.save()

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


