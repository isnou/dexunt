from .functions import text_selector, session_manager

def manager(request):
    session_manager(language = request.session.get('language'))

    return {
        # ---------------------------  topbar --------------------------- #
        'login_txt': text_selector(
            en_text="Login",
            fr_text="Se connecter",
            ar_text="تسجيل",
        ),
        # --------------------------  language -------------------------- #
        'selected_language': request.session.get('selected_language', None),
        'second_language': request.session.get('second_language', None),
        'third_language': request.session.get('third_language', None),
    }