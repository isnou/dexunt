from django.shortcuts import render, redirect
from globals.functions import text_selector, session_manager
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


# ---------------------------- renders ---------------------------- #
def home_page(request):# (home-page)
    session_manager(init=True, source='home-page')
    url = request.session.get('direction') + "/home/main.html"

    context = {
        # [parent template] --------------------------------------- #
        'login_txt': text_selector(
            en_text="Login",
            fr_text="Se connecter",
            ar_text="تسجيل",
        ),

        # [child template] ---------------------------------------- #
        # [child template] -> [title block] ----------------------- #
        'page_title_txt': text_selector(
            en_text="Dexunt | Trusted & Professional Craftsmen Finder | Home Page",
            fr_text="Dexunt | Recherche d'artisans de confiance et professionnels | Page d'accueil",
            ar_text="ديكسونت | الباحث الموثوق والمحترف عن الحرفيين | الصفحة الرئيسية",
        ),

        # [child template] -> [content block] -> [main banner] ---- #
        'welcome_txt': text_selector(
            en_text="Trusted craftsmen at your service",
            fr_text="Des artisans de confiance à votre service",
            ar_text="حرفيين موثوقين في خدمتكم",
        ),
        'job_title': {
            'painter_txt': text_selector(
                en_text="painter.",
                fr_text="peintre.",
                ar_text="دهان.",
            ),
            'electrician_txt': text_selector(
                en_text="electrician.",
                fr_text="électricien.",
                ar_text="كهربائي.",
            ),
            'plumber_txt': text_selector(
                en_text="plumber.",
                fr_text="plombièr.",
                ar_text="سباك.",
            ),
            'mason_txt': text_selector(
                en_text="mason.",
                fr_text="maçon.",
                ar_text="بناء.",
            ),
            'CCTV_technician_txt': text_selector(
                en_text="CCTV installer.",
                fr_text="installateur de vidéosurveillance.",
                ar_text="مثبت كاميرات المراقبة.",
            ),
            'AC_technician_txt': text_selector(
                en_text="AC installer.",
                fr_text="installateur de clim.",
                ar_text="مثبت مكيفات.",
            ),
        },
        'message_txt': text_selector(
            en_text="Our platform allows people with repair, renovation or construction projects to easily find trusted and rated craftsmen throughout Algeria.",
            fr_text="Notre plateforme permet aux personnes ayant des projets de réparation, de rénovation ou de construction de trouver facilement des artisans de confiance et notés partout en Algérie.",
            ar_text="تتيح منصتنا للأشخاص الذين لديهم مشاريع إصلاح أو تجديد أو بناء العثور بسهولة على حرفيين موثوقين ومصنفين في جميع أنحاء الجزائر.",
        ),
        'how_it_works_txt': text_selector(
            en_text="How it works",
            fr_text="Comment ça fonctionne",
            ar_text="كيف تعمل",
        ),
        'get_started_txt': text_selector(
            en_text="Get started",
            fr_text="Commencer",
            ar_text="إبدء",
        ),
        'how_it_works_video_link': 'https://www.youtube.com/watch?v=d4eDWc8g0e0',

        # [child template] -> [modals block] -> [authentication] -- #
        'login_form': LoginForm(),
        'signup_form': SignupForm(),
    }
    return render(request, url, context)
#                                                                   #
# ----------------------------------------------------------------- #


# ------------------------- redirections -------------------------- #
def change_language(request):# (change-language) #
    session_manager(language=request.GET.get('language', None))
    return redirect(request.session.get('source', None))
#                                                                   #
def router(request):# (router) #
    if request.session.get('source', None) == 'login':
        if request.user.is_superuser:
            return redirect('admin-home')
        if request.user.type == 'blank':
            return redirect('edit-profile', 'page')

    if request.session.get('source', None) == 'home-page':
        if request.user.is_superuser:
            return redirect('admin-home')
        if request.user.type == 'blank':
            return redirect('edit-profile', 'page')
#                                                                   #
# ----------------------------------------------------------------- #



