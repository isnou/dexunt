from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Content(models.Model):
    # ------- language
    lang = models.CharField(max_length=20, unique=True)
    # ------- first banner

    def __str__(self):
        return self.lang
