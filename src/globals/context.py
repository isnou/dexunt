from .functions import text_selector, session_manager

def manager(request):
    if not request.session.get('direction', None):
        request.session['direction'] = 'ltr'

    if not request.session.get('language', None):
        request.session['language'] = 'en-us'

    session_manager(language = request.session.get('language'))

    return {
        'test': text_selector(
            'Track my order',
            'Suivre ma commande',
            'تابع طلبي'
        ),

        # --------------------------  language -------------------------- #
        'selected_language': request.session.get('selected_language', None),
        'second_language': request.session.get('second_language', None),
        'third_language': request.session.get('third_language', None),
    }