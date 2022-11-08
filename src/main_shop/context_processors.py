def extras(request):
    en = {
        'title': "Dexunt Home Page",
        'title-info': "Online Shopping Gifts & Deco",
        'track-my-order': "track my order",
        'search-text': "search products here",
        'all-category': "all",
    }

    fr = {
        'title': "Page d'accueil de Dexunt",
        'title-info': "Shopping en ligne cadeaux et déco",
        'track-my-order': "suivre ma commande",
        'search-text': "rechercher des produits ici",
        'all-category': "tout",
    }

    ar = {
        'title': "الصفحة الرئيسية لـ Dexunt",
        'title-info': "التسوق عبر الإنترنت هدايا وديكو",
        'track-my-order': "تابع طلبي",
        'search-text': "البحث عن المنتجات هنا",
        'all-category': "الكل",
    }
    return en, fr, ar
