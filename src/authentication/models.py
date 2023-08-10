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
    ref = models.CharField(max_length=10, unique=True, null=True)
    secret_key = models.CharField(max_length=6, unique=True, null=True)
    tags = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    requested_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='payments_requested', null=True)  # -- to be done with a member
    confirmed_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='payments_confirmed', null=True)  # -- to be done with a member
    wallet = models.ForeignKey(
        'authentication.Wallet', on_delete=models.CASCADE, related_name='transactions', null=True) # -- to be done with a member wallet
    # ----- content ----- #
    title = models.CharField(max_length=500, blank=True, null=True)
    amount = models.IntegerField(default=0)
    requested_at = models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmed = models.BooleanField(default=True)  # -- (confirmed = False) => requested
    add = models.BooleanField(default=True)  # -- (add = False) => remove
    # ----- functions ----- #
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save()
        if not self.ref:
            self.ref = str(self.id+1).zfill(10)
        super().save()
    def generate_secret_key(self):
        self.secret_key = functions.serial_number_generator(6)
        super().save()
#                                                                        #
def transactions_filter(request, new_filter):
    if new_filter:
        request.session['transactions_filter'] = new_filter

    if request.session.get('transactions_filter', None) == 'all':
        return request.user.wallet.transactions.all()
    if request.session.get('transactions_filter', None) == 'costumers':
        return Transaction.objects.all().filter(is_customer=True)
#                                                                        #
def requested_payments():
    return Transaction.objects.all().filter(title='provider-payment-request')
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
        for transaction in self.transactions.all():
            if transaction.confirmed:
                if transaction.add:
                    self.balance += transaction.amount
                else:
                    self.balance -= transaction.amount
        super().save()
#                                                                        #
class DeliveryAddress(models.Model):
    # ----- Technical ----- #
    default = models.BooleanField(default=False)
    # ----- relations ----- #
    municipality = models.ForeignKey(
        'home.Municipality', on_delete=models.CASCADE, related_name='delivery_addresses', null=True)
    user = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='delivery_addresses', null=True)
    # ---- content ---- #
    title = models.CharField(max_length=100, blank=True, null=True)
    delivery_type = models.CharField(max_length=100, default='HOME')
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
    is_cash_manager = models.BooleanField(default=False)
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
        self.file_name = 'profile_photos' + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/'
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
        if new_role == 'cash':
            self.is_cash_manager = True
        super().save()
    def new_address(self, request, municipality):
        if request.method == 'POST':
            title = request.POST.get('title', False)
            default = request.POST.get('default', False)
            new_address = DeliveryAddress(title=title,
                                          municipality=municipality,
                                          user=self)
            if request.POST.get('deliver_type', False):
                new_address.delivery_type = request.POST.get('deliver_type', False)
            if default == 'true':
                for a in self.delivery_addresses.all():
                    a.default = False
                    a.save()
                new_address.default = True
            new_address.save()
    def add_funds(self, title, amount):
        Transaction(wallet=self.wallet,
                    title=title,
                    amount=amount
                    ).save()
        self.wallet.update()
    def request_transaction(self, title, amount, secret_key):
        selected_transaction =  Transaction(confirmed = False,
                                            add=False,
                                            requested_by = self,
                                            requested_at = timezone.now(),
                                            wallet = self.wallet,
                                            title = title,
                                            amount = amount
                                            )
        if secret_key:
            selected_transaction.save()
            selected_transaction.generate_secret_key()
        else:
            selected_transaction.save()
    def confirm_transaction(self, secret_key, transaction_id):
        selected_transaction = Transaction.objects.all().get(id=transaction_id)
        if selected_transaction.secret_key:
            if secret_key == selected_transaction.secret_key:
                selected_transaction.confirmed = True
                selected_transaction.confirmed_at = timezone.now()
                selected_transaction.confirmed_by = self
                selected_transaction.save()
                Transaction(confirmed = True,
                            confirmed_by=selected_transaction.confirmed_by,
                            confirmed_at=selected_transaction.confirmed_at,
                            requested_by = selected_transaction.requested_by,
                            requested_at = selected_transaction.requested_at,
                            wallet = self.wallet,
                            title = title,
                            amount = amount
                            ).save()
        else:
            selected_transaction.confirmed = True
            selected_transaction.confirmed_at = timezone.now()
            selected_transaction.confirmed_by = self
            selected_transaction.save()
            Transaction(confirmed=True,
                        confirmed_by=selected_transaction.confirmed_by,
                        confirmed_at=selected_transaction.confirmed_at,
                        requested_by=selected_transaction.requested_by,
                        requested_at=selected_transaction.requested_at,
                        wallet=self.wallet,
                        title=title,
                        amount=amount
                        ).save()
    # ----- variables ----- #
    def new_orders_count(self):
        if self.is_superuser or self.is_admin or self.is_member:
            count = 0
            for o in Order.objects.all():
                if o.status == 'placed':
                    count += 1
            return count
        if self.is_provider:
            count = 0
            for o in self.store.orders.all():
                if o.status == 'confirmed':
                    count += 1
            return count
    def client_name(self):
        return self.first_name + ' ' + self.last_name
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
#                                                                        #
def reset_users():
    users = User.objects.all()
    carts = Cart.objects.all()
    for c in carts:
        for u in users:
            if c.id == u.cart.id:
                carts = carts.exclude(id=u.cart.id)
    for c in carts:
        if not c.selected_products.all().count():
            if not c.created_at <= timezone.now():
                c.delete()
    for u in users:
        u.wallet.update()
# ---------------------------------------------------------------------- #







