from django.shortcuts import render, redirect
from globals.functions import text_selector, session_manager
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User

def home_page(request):
    session_manager(init=True, source='home-page')
    url = request.session.get('direction') + "/home/main.html"

    context = {
        'welcome_txt': text_selector(
            'trusted tradespersons at your service',
            'des artisans de confiance à votre service',
            'حرفيين موثوقين في خدمتكم',
        ),
        'job_title': {
            'painter_txt': text_selector(
                'painter',
                'peintre',
                'دهان',
            ),
            'electrician_txt': text_selector(
                'electrician',
                'électricien',
                'كهربائي',
            ),
            'plumber_txt': text_selector(
                'plumber',
                'plombière',
                'سباك',
            ),
            'mason_txt': text_selector(
                'mason',
                'maçon',
                'بناء',
            ),
            'CCTV_technician_txt': text_selector(
                'CCTV installer',
                'installateur de vidéosurveillance',
                'مثبت كاميرات المراقبة',
            ),
            'AC_technician_txt': text_selector(
                'AC installer',
                'installateur de clim',
                'مثبت مكيفات',
            ),
        }
    }
    return render(request, url, context)

def change_language(request):
    session_manager(language=request.GET.get('language', None))
    return redirect(request.session.get('source', None))




