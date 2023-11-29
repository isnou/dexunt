from globals.functions import text_selector

def session_language(request):
    return {
        'language': request.session.get('language', None),
        'test': text_selector('Track my order', 'Suivre ma commande', 'تابع طلبي'),
    }