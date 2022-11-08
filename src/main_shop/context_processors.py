def extras(request):
    context = {
        'en.home_title': "Dexunt Home Page",
        'en.home_title_info': "Online Shopping Gifts & Deco",
        'en.track_my_order': "track my order",
        'en.search_text': "search products here",
        'en.all_category': "all",
        'fr.home_title': "Page d'accueil de Dexunt",
        'fr.home_title_info': "Shopping en ligne cadeaux et déco",
        'fr.track_my_order': "suivre ma commande",
        'fr.search_text': "rechercher des produits ici",
        'fr.all_category': "tout",
        'ar.home_title': "الصفحة الرئيسية لـ Dexunt",
        'ar.home_title_info': "التسوق عبر الإنترنت هدايا وديكو",
        'ar.track_my_order': "تابع طلبي",
        'ar.search_text': "البحث عن المنتجات هنا",
        'ar.all_category': "الكل",
    }
    return context
