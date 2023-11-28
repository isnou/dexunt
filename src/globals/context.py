from globals.functions import text_selector

def session_language(request):

    return {
        'test':text_selector('Track my order', 'Suivre ma commande', 'تابع طلبي'),
    }