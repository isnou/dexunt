def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    language = request.session.get('language')

    if language == 'en-us':
        track_my_order = 'track my order'
    elif language == 'fr-fr':
        track_my_order = 'suivre ma commande'
    elif language == 'ar-dz':
        track_my_order = 'تابع طلبي'
    else:
        track_my_order = ''

    return {
        'track_my_order': track_my_order
    }