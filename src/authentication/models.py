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
    # many transactions #
    # one user #
    # ----- content ----- #
    balance = models.IntegerField(default=0)
    # ----- functions ----- #
    def update(self):
        self.balance = 0
        for transaction in self.transaction.all():
            self.balance += transaction.amount
        super().save()
#                                                            #
class DeliveryAddress(models.Model):
    # ---- content ---- #
    title = models.CharField(max_length=60, default='home')
    state = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    detail = models.CharField(max_length=128, blank=True, null=True)
    default = models.BooleanField(default=False)
    # ----- relations ----- #
    municipality = models.ForeignKey(
        'home.Municipality', on_delete=models.CASCADE, related_name='delivery_addresses', null=True)
    user = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='delivery_addresses', null=True)
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
    sale = models.IntegerField(default=0)
    # ----- relations ----- #
    # many selected_products #
    # many delivery_addresses #
    # many order_set #
    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.PROTECT,
        null=True
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    store = models.OneToOneField(
        Store,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
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
    def new_orders(self):
        if self.is_superuser or self.is_admin or self.is_member:
            count = 0
            for o in Order.objects.all():
                if o.status() == 'confirmation':
                    count += 1
            return count
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







