import random, string
from main_home.models import Cart

def serial_number_generator(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def get_cart(request):
    if not request.user.is_authenticated:
        if not request.session.get('cart_ref', None):
            selected_cart = Cart()
            selected_cart.save()
            request.session['cart_ref'] = selected_cart.ref
        else:
            ref = request.session.get('cart_ref')
            if Cart.objects.all().filter(ref=ref).exists():
                selected_cart = Cart.objects.all().get(ref=ref)
            else:
                selected_cart = Cart()
                selected_cart.save()
                request.session['cart_ref'] = selected_cart.ref
    else:
        if Cart.objects.all().filter(user_token=request.user.user_token).exists():
            selected_cart = Cart.objects.all().get(user_token=request.user.user_token)
        else:
            selected_cart = Cart(user_token=request.user.user_token)
            selected_cart.save()
    return selected_cart
