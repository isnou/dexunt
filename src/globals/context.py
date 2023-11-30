from .functions import text_selector, session_manager

def manager(request):
    session_manager(language = request.session.get('language'))

    return {
        # --------------------------  language -------------------------- #
        'selected_language': request.session.get('selected_language', None),
        'second_language': request.session.get('second_language', None),
        'third_language': request.session.get('third_language', None),
    }

def top_bar():
    return {
        'login': text_selector(
            'login',
            'se connecter',
            'تسجيل'
        ),
    }