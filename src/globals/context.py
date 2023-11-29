from .functions import text_selector

def text(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'

    if request.session.get('language') == 'en-us':
        second_language = {
            'title': 'Français',
            'key': 'fr-fr',
        }
        third_language = {
            'title': 'العربية',
            'key': 'ar-dz',
        }
    elif request.session.get('language') == 'fr-fr':
        second_language = {
            'title': 'english',
            'key': 'en-us',
        }
        third_language = {
            'title': 'العربية',
            'key': 'ar-dz',
        }
    elif request.session.get('language') == 'ar-dz':
        second_language = {
            'title': 'english',
            'key': 'en-us',
        }
        third_language = {
            'title': 'français',
            'key': 'fr-fr',
        }
    else:
        second_language = None
        third_language = None


    return {
        'test': text_selector(
            'Track my order',
            'Suivre ma commande',
            'تابع طلبي'
        ),
        # -------------  language ------------- #
        'selected_language': request.session.get('selected_language'),
        'second_language': request.session.get('second_language'),
        'third_language': request.session.get('third_language'),
    }