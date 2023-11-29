from globals.functions import text_selector

def session_language(request):
    language = request.GET.get('language', False)

    return {
        'language': language,
        'test': text_selector('Track my order', 'Suivre ma commande', 'تابع طلبي'),
    }