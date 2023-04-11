from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from sell_manager.models import Order, UserCart
from main_shop.models import WishedProduct, Server
from PIL import Image
