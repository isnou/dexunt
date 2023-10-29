from add_ons.functions import text_selector

def language(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    selected_language = request.session.get('language')
    en_us = False
    fr_fr = False
    ar_dz = False

    if selected_language == 'en-us':
        en_us = True
    if selected_language == 'fr-fr':
        fr_fr = True
    if selected_language == 'ar-dz':
        ar_dz = True


    return {
        'txt_track_my_order':text_selector('Track my order', 'Suivre ma commande', 'تابع طلبي', selected_language),
        'txt_search_holder':text_selector('Search for products', 'Rechercher des produits', 'البحث عن المنتجات', selected_language),
        'en_us': en_us,
        'fr_fr': fr_fr,
        'ar_dz': ar_dz,
    }