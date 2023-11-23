import random, string
from management.models import Product, Tag

def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def text_selector(en_text, fr_text, ar_text, language):
    if language == 'en-us':
        return en_text
    if language == 'fr-fr':
        return fr_text
    if language == 'ar-dz':
        return ar_text

def collect_tags():
    for p in Product.objects.all():
        p.collect_tags()
        
    for t in Tag.objects.all():
        if t.product.all().count() < 2:
            t.delete()