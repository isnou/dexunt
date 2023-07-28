from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from add_ons import functions
from django.utils import timezone, dateformat
from PIL import Image
from home.models import Cart, Order
from management.models import Store



# ------------------------------ Setting ------------------------------- #
class Transaction(models.Model):
    # ----- Technical ----- #
    hook = models.CharField(max_length=24, null=True)
    # ----- relations ----- #
    wallet = models.ForeignKey(
        'authentication.Wallet', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    title = models.CharField(max_length=500, blank=True, null=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
#                                                                        #
class Wallet(models.Model):
    # ----- relations ----- #
    # related to many transactions #
    # ----- content ----- #
    balance = models.IntegerField(default=0)
    # ----- functions ----- #
    def update(self):
        self.balance = 0
        for transaction in self.transaction.all():
            self.balance += transaction.amount
        super().save()
# ---------------------------------------------------------------------- #



# -------------------------------- User -------------------------------- #
class User(AbstractUser):
    # ----- Technical ----- #
    is_blacklisted = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    # ----- #
    is_customer = models.BooleanField(default=True)
    is_provider = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # ----- #
    tags = models.CharField(max_length=5000, blank=True, null=True)
    points = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    token = models.CharField(max_length=24, unique=True, null=True)
    # ----- relations ----- #
    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.PROTECT,
        null=True
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.PROTECT,
        null=True
    )
    store = models.OneToOneField(
        Store,
        on_delete=models.PROTECT,
        null=True
    )
    order = models.ManyToManyField(Order, blank=True)
    # ----- media ----- #
    file_name = models.CharField(max_length=300, blank=True, null=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    profile_photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # ----- content ----- #
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    # ----- functions ----- #
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = functions.serial_number_generator(24).upper()
        self.file_name = 'profile_photos' + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/' + self.token + '/'
        if not self.wallet:
            new_wallet = Wallet()
            new_wallet.save()
            self.wallet = new_wallet
        if not self.cart:
            new_cart = Cart()
            new_cart.save()
            self.cart = new_cart
        if not self.store:
            if self.is_provider:
                new_store = Store()
                new_store.save()
                self.store = new_store
        self.tags = ''
        if self.first_name:
            self.tags += (', ' + self.first_name)
        if self.last_name:
            self.tags += (', ' + self.last_name)
        if self.province:
            self.tags += (', ' + self.province)
        if self.municipality:
            self.tags += (', ' + self.municipality)
        super().save()
    def change_role(self, new_role):
        self.is_customer = False
        if new_role == 'seller':
            self.is_seller = True
        if new_role == 'provider':
            self.is_provider = True
        if new_role == 'member':
            self.is_member = True
        super().save()

#                                                                        #
def users_filter(request, users_list, new_filter):
    if new_filter:
        request.session['users_filter'] = new_filter

    if request.session.get('users_filter', None) == 'all':
        return users_list
    if request.session.get('users_filter', None) == 'costumers':
        return users_list.filter(is_customer=True)
    if request.session.get('users_filter', None) == 'members':
        return users_list.filter(is_member=True)
    if request.session.get('users_filter', None) == 'sellers':
        return users_list.filter(is_seller=True)
    if request.session.get('users_filter', None) == 'providers':
        return users_list.filter(is_provider=True)
    if request.session.get('users_filter', None) == 'blacklist':
        return users_list.filter(is_blacklisted=True)
# ---------------------------------------------------------------------- #







