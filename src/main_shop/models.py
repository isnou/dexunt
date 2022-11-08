from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Content(models.Model):
    lang = models.CharField(max_length=20, unique=True)
    home_page_title = models.CharField(max_length=200)

    def __str__(self):
        return self.lang
