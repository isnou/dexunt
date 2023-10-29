from add_ons.functions import text_selector

def session_language(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    language = request.session.get('language')


    return {
        'txt_track_my_order':text_selector('Track my order', 'Suivre ma commande', 'تابع طلبي', language),
        'txt_search_holder':text_selector('Search for products', 'Rechercher des produits', 'البحث عن المنتجات', language),
        'language': language,
    }