def extras(request):
    en = {
        'home_title': "Dexunt Home Page",
        'home_title_info': "Online Shopping Gifts & Deco",
        'track_my_order': "track my order",
        'search_text': "search products here",
        'all_category': "all",
    }

    fr = {
        'home_title': "Page d'accueil de Dexunt",
        'home_title_info': "Shopping en ligne cadeaux et déco",
        'track_my_order': "suivre ma commande",
        'search_text': "rechercher des produits ici",
        'all_category': "tout",
    }

    ar = {
        'home_title': "الصفحة الرئيسية لـ Dexunt",
        'home_title_info': "التسوق عبر الإنترنت هدايا وديكو",
        'track_my_order': "تابع طلبي",
        'search_text': "البحث عن المنتجات هنا",
        'all_category': "الكل",
    }
    return en, fr, ar
