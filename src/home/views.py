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
            'Trusted craftsmen at your service',
            'Des artisans de confiance à votre service',
            'حرفيين موثوقين في خدمتكم',
        ),
        'job_title': {
            'painter_txt': text_selector(
                'Painter.',
                'Peintre.',
                'دهان.',
            ),
            'electrician_txt': text_selector(
                'Electrician.',
                'Électricien.',
                'كهربائي.',
            ),
            'plumber_txt': text_selector(
                'Plumber.',
                'Plombière.',
                'سباك.',
            ),
            'mason_txt': text_selector(
                'Mason.',
                'Maçon.',
                'بناء.',
            ),
            'CCTV_technician_txt': text_selector(
                'CCTV Installer.',
                'Installateur de Vidéosurveillance.',
                'مثبت كاميرات المراقبة.',
            ),
            'AC_technician_txt': text_selector(
                'AC Installer.',
                'Installateur de Clim.',
                'مثبت مكيفات.',
            ),
        },
        'message_txt': text_selector(
            'Our platform allows people with repair, renovation or construction projects to easily find trusted and rated craftsmen throughout Algeria.',
            'Notre plateforme permet aux personnes ayant des projets de réparation, de rénovation ou de construction de trouver facilement des artisans de confiance et notés partout en Algérie.',
            'تتيح منصتنا للأشخاص الذين لديهم مشاريع إصلاح أو تجديد أو بناء العثور بسهولة على حرفيين موثوقين ومصنفين في جميع أنحاء الجزائر.',
        ),
    }
    return render(request, url, context)

def change_language(request):
    session_manager(language=request.GET.get('language', None))
    return redirect(request.session.get('source', None))




