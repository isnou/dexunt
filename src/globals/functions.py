def session_manager(**kwargs):
    if kwargs.get('language', None) == 'en-us':
        global_request.session['selected_language'] = {
            'title': 'english',
            'key': 'en-us',
        }
        global_request.session['second_language'] = {
            'title': 'français',
            'key': 'fr-fr',
        }
        global_request.session['third_language'] = {
            'title': 'العربية',
            'key': 'ar-dz',
        }
    if kwargs.get('language', None) == 'fr-fr':
        global_request.session['selected_language'] = {
            'title': 'français',
            'key': 'fr-fr',
        }
        global_request.session['second_language'] = {
            'title': 'english',
            'key': 'en-us',
        }
        global_request.session['third_language'] = {
            'title': 'العربية',
            'key': 'ar-dz',
        }
    if kwargs.get('language', None) == 'ar-dz':
        global_request.session['selected_language'] = {
            'title': 'العربية',
            'key': 'ar-dz',
        }
        global_request.session['second_language'] = {
            'title': 'english',
            'key': 'en-us',
        }
        global_request.session['third_language'] = {
            'title': 'français',
            'key': 'fr-fr',
        }
#                                                            #
def text_selector(en_text, fr_text, ar_text):
    if not global_request.session.get('language', None):
        global_request.session['language'] = 'en-us'
    language = global_request.session.get('language')

    if language == 'en-us':
        return en_text
    if language == 'fr-fr':
        return fr_text
    if language == 'ar-dz':
        return ar_text
#                                                            #
def serial_number_generator(length):
    import random, string

    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
#                                                            #
def collect_tags(tags):
    from management.models import Product, Tag

    for tag in tags.split():
        tag = ''.join(filter(str.isalpha, tag))
        if len(tag) > 2:
            if not Tag.objects.all().filter(title__icontains=tag).exists():
                Tag(title=tag).save()
    for p in Product.objects.all():
        p.collect_tags()
#                                                            #
def clean_tags():
    from management.models import Tag

    for t in Tag.objects.all():
        if t.product.all().count() < 2:
            t.delete()