from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from add_ons import functions
from django.utils import timezone, dateformat
from PIL import Image
from home.models import Cart, Order, SelectedProduct
from management.models import Store


# ------------------------------ Setting ------------------------------- #
class Transaction(models.Model):
    # ----- Technical ----- #
    ref = models.CharField(max_length=10, unique=True, null=True)
    secret_key = models.CharField(max_length=6, blank=True, unique=True, null=True)
    tags = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    requested_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='payments_requested', blank=True, null=True)  # -- to be done with a member
    confirmed_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='payments_confirmed', blank=True, null=True)  # -- to be done with a member
    wallet = models.ForeignKey(
        'authentication.Wallet', on_delete=models.CASCADE, related_name='transactions', null=True) # -- to be done with a member wallet
    # ----- content ----- #
    title = models.CharField(max_length=500, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
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
        if self.title.startswith('paid-order'):
            self.confirmed = True
        super().save()
    def generate_secret_key(self):
        self.secret_key = functions.serial_number_generator(6)
        super().save()
    # ----- variables ----- #
    def order_payment(self):
        if self.title.startswith('paid-order'):
            return True
    def order_ref(self):
        return self.title[11:]
#                                                                        #
def transactions_filter(request, new_filter):
    if new_filter:
        request.session['transactions_filter'] = new_filter
    if request.session.get('transactions_filter', None) == 'all':
        return request.user.wallet.transactions.all()
    if request.session.get('transactions_filter', None) == 'costumers':
        return Transaction.objects.all().filter(is_customer=True)
#                                                                        #
def transactions_select(action):
    if action == 'member-requests':
        return Transaction.objects.all().filter(title='member-payment-request').filter(confirmed=False)
    if action == 'provider-requests':
        return Transaction.objects.all().filter(title='provider-payment-request').filter(confirmed=False)
    if action == 'funds-transfer':
        return Transaction.objects.all().filter(title='member-funds-transfer').filter(confirmed=False)
    if action == 'sale-transactions':
        return Transaction.objects.all().filter(title__icontains='paid-order')
    if action == 'sales-income':
        value = 0
        for t in Transaction.objects.all().filter(title__icontains='paid-order'):
            value += t.amount
        return value
    if action == 'member-transactions':
        return User.objects.all().filter(is_member=True)
    if action == 'members-income':
        value = 0
        for u in User.objects.all().filter(is_member=True):
            value += u.wallet.balance
        return value
    if action == 'provider-transactions':
        return Store.objects.all()
    if action == 'providers-income':
        value = 0
        for s in Store.objects.all():
            value += s.balance()
        return value
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
    content = models.CharField(max_length=500, blank=True, null=True)
# ---------------------------------------------------------------------- #


# -------------------------------- User -------------------------------- #
class User(AbstractUser):
    # ----- Technical ----- #
    is_blacklisted = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    # ----- #
    is_customer = models.BooleanField(default=True)
    is_provider = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_cash_manager = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    # ----- relations ----- #
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
    def set_address_as_default(self, request):
        address_id = request.GET.get('address_id')
        selected_address = self.delivery_addresses.all().get(id=address_id)
        for a in self.delivery_addresses.all():
            a.default = False
            a.save()
        selected_address.default = True
        selected_address.save()
    def edit_address(self, request):
        if request.method == 'POST':
            content = request.POST.get('content', False)
            address_id = request.POST.get('address_id')
            selected_address = self.delivery_addresses.all().get(id=address_id)
            selected_address.content = content
            selected_address.save()
    def new_address(self, request, municipality):
        if request.method == 'POST':
            content = request.POST.get('content', False)
            default = request.POST.get('default', False)
            new_address = DeliveryAddress(content=content,
                                          municipality=municipality,
                                          user=self)
            if default == 'true':
                for a in self.delivery_addresses.all():
                    a.default = False
                    a.save()
                new_address.default = True
            new_address.save()
    def add_funds(self, title, amount):
        Transaction(confirmed = False,
                    wallet=self.wallet,
                    title=title,
                    amount=amount
                    ).save()
        self.wallet.update()
    def request_transaction(self, title, amount, secret_key):
        selected_transaction =  Transaction(confirmed = False,
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
        if selected_transaction.title == 'provider-payment-request':
            if secret_key == selected_transaction.secret_key:
                selected_transaction.confirmed = True
                selected_transaction.add = False
                selected_transaction.confirmed_at = timezone.now()
                selected_transaction.confirmed_by = self
                selected_transaction.save()
                Transaction(confirmed = True,
                            add=False,
                            confirmed_by=selected_transaction.confirmed_by,
                            confirmed_at=selected_transaction.confirmed_at,
                            requested_by = selected_transaction.requested_by,
                            requested_at = selected_transaction.requested_at,
                            wallet = self.wallet,
                            title = selected_transaction.title,
                            amount = selected_transaction.amount
                            ).save()
            selected_transaction.requested_by.wallet.update()
        if selected_transaction.title == 'member-payment-request':
            selected_transaction.confirmed = True
            selected_transaction.confirmed_at = timezone.now()
            selected_transaction.confirmed_by = self
            selected_transaction.save()
            Transaction(confirmed = True,
                        add=False,
                        confirmed_by=selected_transaction.confirmed_by,
                        confirmed_at=selected_transaction.confirmed_at,
                        requested_by = selected_transaction.requested_by,
                        requested_at = selected_transaction.requested_at,
                        wallet = self.wallet,
                        title = selected_transaction.title,
                        amount = selected_transaction.amount
                        ).save()
            selected_transaction.requested_by.wallet.update()
        if selected_transaction.title == 'funds-added':
            selected_transaction.confirmed = True
            selected_transaction.confirmed_at = timezone.now()
            selected_transaction.confirmed_by = self
            selected_transaction.save()
        if selected_transaction.title == 'member-funds-transfer':
            selected_transaction.add = False
            selected_transaction.confirmed = True
            selected_transaction.confirmed_at = timezone.now()
            selected_transaction.confirmed_by = self
            selected_transaction.requested_by = selected_transaction.wallet.user
            selected_transaction.requested_at = selected_transaction.created_at
            selected_transaction.save()
            Transaction(confirmed = True,
                        confirmed_by=selected_transaction.confirmed_by,
                        confirmed_at=selected_transaction.confirmed_at,
                        requested_by = selected_transaction.requested_by,
                        requested_at = selected_transaction.requested_at,
                        wallet = self.wallet,
                        title = selected_transaction.title,
                        amount = selected_transaction.amount
                        ).save()
            selected_transaction.wallet.update()
        self.wallet.update()
    # ----- variables ----- #
    def client_name(self):
        return self.first_name + ' ' + self.last_name
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
    def unreviewed_orders(self):
        return self.all_orders.all().filter(status='paid')
    def unreviewed_orders_count(self):
        count = 0
        for o in self.unreviewed_orders():
            for p in o.unreviewed_products().all():
                if not p.status == 'refund_request':
                    count += 1
        return count
    def refund_requests_count(self):
        if self.is_superuser or self.is_admin or self.is_member:
            return SelectedProduct.objects.all().filter(status='refund_request').count()
    def refunds(self):
        if self.is_superuser or self.is_admin or self.is_member:
            return SelectedProduct.objects.all().filter(status='refund_request')
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
        u.cart.ref = None
        u.cart.save()
# ---------------------------------------------------------------------- #







