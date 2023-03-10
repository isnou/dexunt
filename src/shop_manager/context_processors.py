from .models import Product, ShowcaseProduct


def shop_manager_content(request):
    try:
        shop_products_list = ShowcaseProduct.objects.all()
    except ShowcaseProduct.DoesNotExist:
        raise Http404("No products")

    try:
        all_products = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No products")

    #showcase_products = raw_products_list.exclude(publish=False)
    #best_sellers = showcase_products.order_by('-sell_rate')[:4]
    #top_rated = showcase_products.order_by('-review_rate')[:4]
    #new_arrivals = showcase_products.order_by('-updated_at')[:4]
    return {
        'products' : products,
    }
