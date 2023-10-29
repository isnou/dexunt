from add_ons.functions import text_selector

def language(request):

    return {
        'txt_track_my_order':text_selector('track my order', 'suivre ma commande', 'تابع طلبي'),
        'language': request.session.get('language'),
    }