from django.db import models
from add_ons import functions
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# ------------------------------------- Orders -------------------------------- #
class SelectedProduct(models.Model):
    # --------------------------------- collection technical informations ----------------------
    delivery = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    # --------------------------------- media --------------------------------------------------
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # --------------------------------- info ---------------------------------------------------
    token = models.CharField(max_length=24, null=True)
    option_id = models.PositiveIntegerField(blank=True, null=True)
    variant_id = models.PositiveIntegerField(blank=True, null=True)

    en_name = models.CharField(max_length=400, blank=True, null=True)
    fr_name = models.CharField(max_length=400, blank=True, null=True)
    ar_name = models.CharField(max_length=400, blank=True, null=True)

    en_detail = models.CharField(max_length=400, blank=True, null=True)
    fr_detail = models.CharField(max_length=400, blank=True, null=True)
    ar_detail = models.CharField(max_length=400, blank=True, null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity_issue = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save()

class Coupon(models.Model):
    # --------------------------------- technical details --------------------------------------
    type = models.CharField(default='subtractive', max_length=20, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # --------------------------------- product information ------------------------------------
    code = models.CharField(max_length=20, unique=True, null=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.type == 'subtractive':
            if self.value < 0:
                self.value = 0
        elif self.type == 'percentage':
            if self.value < 0:
                self.value = 0
            elif self.value > 100:
                self.value = 100
        super().save()

    def clean(self):
        if self.valid_until <= timezone.now():
            self.is_active = False
        if self.quantity == 0:
            self.is_active = False
        super().save()

class Cart(models.Model):
    # --------------------------------- technical details --------------------------------------
    ref = models.CharField(max_length=20, unique=True, null=True)
    product = models.ManyToManyField(SelectedProduct, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_token = models.CharField(max_length=24, blank=True, null=True)
    # --------------------------------- product information ------------------------------------
    sub_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # --------------------------------- coupon information -------------------------------------
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    coupon_type = models.CharField(max_length=20, blank=True, null=True)
    coupon_value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = functions.serial_number_generator(20).upper()
        super().save()

    def update_prices(self):
        new_price = 0
        for product in self.product.all():
            new_price += product.total_price
        self.sub_total_price = new_price
        self.total_price = new_price
        if self.coupon_type == 'subtractive':
            self.total_price = self.sub_total_price - self.coupon_value
        if self.coupon_type == 'percentage':
            self.total_price = self.sub_total_price - (( self.sub_total_price * self.coupon_value ) / 100)
        super().save()

    def delete_products(self):
        for product in self.product.all():
            product.delete()
        super().save()

class Order(models.Model):
    # --------------------------------- order technical informations ---------------------------
    cart_ref = models.CharField(max_length=20, blank=True, null=True)
    ref = models.CharField(max_length=6, unique=True, null=True)
    type = models.CharField(max_length=200, default='REGULAR')
    # -- order_types : REGULAR - BOX

    status = models.CharField(max_length=100, default='INCOMPLETE')
    # -- status : INCOMPLETE - FULFILLED -

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_token = models.CharField(max_length=24, blank=True, null=True)
    # --------------------------------- client info --------------------------------------------
    product = models.ManyToManyField(SelectedProduct, blank=True)
    client_name = models.CharField(max_length=300, blank=True, null=True)
    client_phone = PhoneNumberField(blank=True)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    # --------------------------------- order info ---------------------------------------------
    points = models.IntegerField(default=0)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    coupon_value = models.IntegerField(default=0, null=True)
    coupon_type = models.CharField(max_length=20, blank=True, null=True)
    # -- coupon_types :  SUBTRACTIVE - PERCENTAGE

    delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    delivery_type = models.CharField(max_length=100, default='HOME')
    # -- delivery_types :  TO-HOME - TO-DESK

    sub_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # --------------------------------- options ------------------------------------------------
    additional_information = models.CharField(max_length=500, blank=True, null=True)
    gift_packaging = models.BooleanField(default=False)
    theme = models.CharField(max_length=100, default='SIMPLE')
    # -- themes :  STANDARD - BIRTHDAY - WEDDING - BIRTH

    occasion = models.CharField(max_length=100, default='UNDEFINED')
    # -- occasions :  UNDEFINED - BIRTHDAY - WEDDING - BIRTH

    secured = models.BooleanField(default=False)
    receiver_name = models.CharField(max_length=300, blank=True, null=True)
    receiver_message = models.CharField(max_length=500, blank=True, null=True)
    quantity_issue = models.BooleanField(default=False)

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
                if self.coupon_type == 'subtractive':
                    self.total_price = self.sub_total_price - self.coupon_value + self.delivery_price
                if self.coupon_type == 'percentage':
                    self.total_price = self.sub_total_price - (( self.sub_total_price * self.coupon_value ) / 100) + self.delivery_price
            else:
                if self.coupon_type == 'subtractive':
                    self.total_price = self.sub_total_price - self.coupon_value
                if self.coupon_type == 'percentage':
                    self.total_price = self.sub_total_price - (( self.sub_total_price * self.coupon_value ) / 100)
        super().save()

    def delete_products(self):
        for product in self.product.all():
            product.delete()
        super().save()

# ------------------------------------- Shipping ------------------------------ #
class Municipality(models.Model):
    # --------------------------------- shipping details ---------------------------------------
    en_name = models.CharField(max_length=200, blank=True, null=True)
    fr_name = models.CharField(max_length=200, blank=True, null=True)
    ar_name = models.CharField(max_length=200, blank=True, null=True)

    en_home_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    fr_home_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    ar_home_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    home_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    en_desk_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    fr_desk_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    ar_desk_delivery_time = models.CharField(max_length=200, blank=True, null=True)
    desk_delivery_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Municipalities"

class Province(models.Model):
    # --------------------------------- shipping details ---------------------------------------
    en_name = models.CharField(max_length=200, blank=True, null=True)
    fr_name = models.CharField(max_length=200, blank=True, null=True)
    ar_name = models.CharField(max_length=200, blank=True, null=True)

    municipality = models.ManyToManyField(Municipality, blank=True)

# ----------------------------------- Functions ------------------------------- #
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
        if Cart.objects.all().filter(user_token=request.user.user_token).exists():
            selected_cart = Cart.objects.all().get(user_token=request.user.user_token)
        else:
            selected_cart = Cart(user_token=request.user.user_token)
            selected_cart.save()
    return selected_cart

def add_product_to_cart(cart, variant, option):
    if cart.product.all().filter(option_id=option.id).exists():
        selected_cart_product = cart.product.all().get(option_id=option.id)
        selected_cart_product.quantity += 1
        selected_cart_product.save()
    else:
        if option.has_image:
            image = option.image
        else:
            album = variant.album.all()[0]
            image = album.image

        cart_product = SelectedProduct(delivery=option.delivery_quotient,
                                       points=option.points,

                                       file_name= 'cart' + variant.en_title + '/' + variant.en_spec + '/' + option.en_value,
                                       image=image,

                                       token=variant.product_token,
                                       option_id=option.id,
                                       variant_id=variant.id,
                                       en_name=variant.en_title,
                                       fr_name=variant.fr_title,
                                       ar_name=variant.ar_title,
                                       en_detail= variant.en_spec + '-' + option.en_value,
                                       fr_detail= variant.fr_spec + '-' + option.fr_value,
                                       ar_detail= variant.ar_spec + '-' + option.ar_value,
                                       )
        if option.discount:
            cart_product.price = option.discount
        else:
            cart_product.price = option.price
        cart_product.save()
        cart.product.add(cart_product)

    cart.update_prices()

def apply_coupon(request, selected_cart, coupon_code):
    code = None
    type = None
    value = None
    if Coupon.objects.all().filter(code=coupon_code).exists():
        coupon = Coupon.objects.all().get(code=coupon_code)
        if coupon.is_active:
            request.session['coupon_message'] = 'success'
            code = coupon.code
            type = coupon.type
            value = coupon.value
        else:
            request.session['coupon_message'] = 'expired'
    else:
        request.session['coupon_message'] = 'wrong'
    selected_cart.coupon_code = code
    selected_cart.coupon_type = type
    selected_cart.coupon_value = value
    selected_cart.update_prices()

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
        if Order.objects.all().filter(user_token=request.user.user_token).exists():
            selected_order = Order.objects.all().get(user_token=request.user.user_token)
        else:
            selected_order = Order(user_token=request.user.user_token,
                                   cart_ref=selected_cart.ref,)
            selected_order.save()

    new_points = 0
    for p in selected_cart.product.all():
        selected_order.product.add(p)
        new_points += p.points

    selected_order.coupon_code = selected_cart.coupon_code
    selected_order.coupon_type = selected_cart.coupon_type
    selected_order.coupon_value = selected_cart.coupon_value
    selected_order.points = new_points
    selected_order.sub_total_price = selected_cart.sub_total_price

    selected_order.update_prices()

    return selected_order

def set_delivery_price(selected_order, selected_municipality, delivery_type):
    if delivery_type == 'home':
        selected_order.delivery_type = 'home'
        selected_order.delivery_price = selected_municipality.home_delivery_price
        selected_order.update_prices()
    if delivery_type == 'desk':
        selected_order.delivery_type = 'desk'
        selected_order.delivery_price = selected_municipality.desk_delivery_price
        selected_order.update_prices()

def place_order(request, selected_cart, selected_order):

    selected_order.status = 'FULFILLED'
    selected_order.update_prices()
    selected_cart.delete()

    request.session['municipality_id_token'] = None
    request.session['order_ref'] = None
    request.session['cart_ref'] = None