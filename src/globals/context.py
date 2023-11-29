from globals.functions import text_selector

def text(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    language = request.session.get('language')

    return {
        'test': text_selector(
            'Track my order',
            'Suivre ma commande',
            'تابع طلبي'
        ),
        'language': language,
    }