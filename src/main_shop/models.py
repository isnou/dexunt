from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Content(models.Model):
    # language
    lang = models.CharField(max_length=20, unique=True)
    # page title
    title = models.CharField(max_length=20, blank=True, unique=True)
    # first banner
    big_banner_small_title = models.CharField(max_length=150, blank=True)
    big_banner_big_title = models.CharField(max_length=150, blank=True)
    big_banner_first_line = models.CharField(max_length=200, blank=True)
    big_banner_first_second = models.CharField(max_length=200, blank=True)
    big_banner_first_third = models.CharField(max_length=200, blank=True)
    big_banner_button_title = models.CharField(max_length=40, blank=True)
    big_banner_button_link = models.URLField(blank=True)

    def __str__(self):
        return self.lang
