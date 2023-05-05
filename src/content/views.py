from django.shortcuts import render, redirect
from add_ons import functions


def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'

    direction = request.session.get('language')
    url = direction + "/home/main-page.html"

    context = {
    }
    return render(request, url, context)

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')