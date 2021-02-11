from products.models import Category, CartProduct, WishList
from .models import SiteInfo


def basic_info(request):
    site_info = SiteInfo.objects.all().first()
    categories = Category.objects.all()[:11]
    if request.user.is_authenticated:
        try:
            cart_count = CartProduct.objects.filter(cart__user=request.user).count()
        except:
            cart_count = 0
        try:
            wish_count = WishList.objects.get(user=request.user).products.count()
        except:
            wish_count = 0
    else:
        cart = request.session.get('cart', None)
        if cart:
            cart_count = len(cart)
        else:
            cart_count = 0
        wish = request.session.get('wish', None)
        if wish:
            wish_count = len(wish)
        else:
            wish_count = 0

    return {'site_info': site_info,
            'categories': categories,
            'cart_count': cart_count,
            'wish_count': wish_count}
