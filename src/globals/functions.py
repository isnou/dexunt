def session_manager(**kwargs):
    if kwargs.get('message', None):
        if kwargs.get('source') == 'login':
            if kwargs.get('success'):
                global_request.session['messages'] = None
            if kwargs.get('login_fail'):
                global_request.session['messages'] = {
                    'color': 'danger',
                    'text':(
                        {
                            'title': text_selector(
                                en_text="Oops !",
                                fr_text="Oups !",
                                ar_text="عفوًا!",
                            ),
                            'content':text_selector(
                                en_text="Looks like something wrong happening.",
                                fr_text="On dirait que quelque chose ne va pas.",
                                ar_text="يبدو أن شيئًا خاطئًا يحدث.",
                            )
                        },
                        text_selector(
                            en_text="password or username incorrect",
                            fr_text="mot de passe ou nom d'utilisateur incorrect",
                            ar_text="كلمة المرور أو اسم المستخدم غير صحيح",
                        ),
                    )
                }
    if kwargs.get('init', None):
        global_request.session['source'] = kwargs.get('source', None)
        if not global_request.session.get('direction', None):
            global_request.session['direction'] = 'ltr'
        if not global_request.session.get('language', None):
            global_request.session['language'] = 'en-us'
        if global_request.session.get('messages', None):
            messages = global_request.session.get('messages')
            global_request.session['messages'] = None
            return messages
    if kwargs.get('language', None) == 'en-us':
        global_request.session['language'] = 'en-us'
        global_request.session['direction'] = 'ltr'
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
        global_request.session['language'] = 'fr-fr'
        global_request.session['direction'] = 'ltr'
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
        global_request.session['language'] = 'ar-dz'
        global_request.session['direction'] = 'rtl'
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
def validation(**kwargs):
    if kwargs.get('username', None):
        from authentication.models import User

        username = kwargs.get('username')
        if len(username) < 6:
            return {
                'content':text_selector(
                    en_text="must have at least 6 characters",
                    fr_text="doit avoir au moins 6 caractères",
                    ar_text="يجب أن يكون على الأقل 6 أحرف",
                ),
                'status':'is-invalid'
            }
        elif len(username) > 18:
            return {
                'content':text_selector(
                    en_text="must not exceed 18 characters",
                    fr_text="ne doit pas dépasser 18 caractères",
                    ar_text="يجب ألا يتجاوز 18 حرفًا",
                ),
                'status':'is-invalid'
            }
        elif User.objects.filter(username=username).exists():
            return {
                'content':text_selector(
                    en_text="existing username, please try another one",
                    fr_text="nom d'utilisateur existant, veuillez en essayer un autre",
                    ar_text="اسم المستخدم موجود، يرجى تجربة اسم مستخدم آخر",
                ),
                'status':'is-invalid'
            }
        else:
            return {
                'content': text_selector(
                    en_text="valid username",
                    fr_text="nom d'utilisateur valide",
                    ar_text="اسم مستخدم صالح",
                ),
                'status': 'is-valid'
            }
#                                                            #
def text_selector(**kwargs):
    language = global_request.session.get('language')

    if language == 'en-us':
        return kwargs.get('en_text', None)
    if language == 'fr-fr':
        return kwargs.get('fr_text', None)
    if language == 'ar-dz':
        return kwargs.get('ar_text', None)
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