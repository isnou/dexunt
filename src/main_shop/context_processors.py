from .models import Intro, Showcase, Category, Directory, Department
from sell_manager.models import Cart
from add_ons import functions


def main_shop_content(request):
    intro = Intro.objects.all().get(id=1)

    if not request.session.get('cart', None):
        request.session['cart'] = functions.serial_number_generator(30).upper()
    cart_ref = request.session.get('cart')

    if Cart.objects.all().filter(ref=cart_ref).exists():
        cart = Cart.objects.all().get(ref=cart_ref)
    else:
        cart = Cart(ref=cart_ref,
                    device=request.user_agent.device.family,
                    operating_system=request.user_agent.os.family + request.user_agent.os.version_string,
                    ip_address=request.META['REMOTE_ADDR'],
                    )
        cart.save()

    try:
        showcases = Showcase.objects.all().order_by('-rank')
    except Showcase.objects.all().DoesNotExist:
        raise Http404("No showcases")

    try:
        departments = Department.objects.all()
    except Department.objects.all().DoesNotExist:
        raise Http404("No directories")

    return {
        'intro': intro,
        'cart': cart,
        'showcases': showcases,
        'departments': departments,
    }
