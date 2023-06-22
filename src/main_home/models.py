from django.db import models
from add_ons import functions
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
    option_id = models.PositiveIntegerField(blank=True, null=True)
    variant_id = models.PositiveIntegerField(blank=True, null=True)

    en_name = models.CharField(max_length=600, blank=True, null=True)
    fr_name = models.CharField(max_length=600, blank=True, null=True)
    ar_name = models.CharField(max_length=600, blank=True, null=True)

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
        for product in self.cart_product.all():
            new_price += product.total_price
        self.sub_total_price = new_price
        self.total_price = new_price
        if self.coupon_type == 'subtractive':
            self.total_price = self.sub_total_price - self.coupon_value
        if self.coupon_type == 'percentage':
            self.total_price = self.sub_total_price - (( self.sub_total_price * self.coupon_value ) / 100)
        super().save()

    def reset(self):
        for product in self.product.all():
            product.delete()
        self.sub_total_price = None
        self.total_price = None
        self.coupon_type = None
        self.coupon_code = None
        self.coupon_value = None
        super().save()

class Order(models.Model):
    # --------------------------------- order technical informations ---------------------------
    order_ref = models.CharField(max_length=12, unique=True, null=True)
    type = models.CharField(max_length=200, default='REGULAR')
    # -- order_types : REGULAR - BOX

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=100, default='FULFILLED')
    # -- status : FULFILLED -

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
    coupon_value = models.IntegerField(default=0)
    coupon_type = models.CharField(max_length=100, default='SUBTRACTION')
    # -- coupon_types :  SUBTRACTION - PERCENTAGE

    shipping_type = models.CharField(max_length=100, default='TO_HOME')
    # -- shipping_types :  TO-HOME - TO-DESK

    sub_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
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
        if not self.order_ref:
            self.order_ref = functions.serial_number_generator(12).upper()
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