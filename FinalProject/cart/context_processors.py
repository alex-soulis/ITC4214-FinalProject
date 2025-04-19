from django.db.models import Sum
from .models import Cart

def cart_item_count(request):
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
    # Sum up quantities (or zero)
    total = (
        cart.items.aggregate(sum=Sum('quantity'))['sum']
        if cart else 0
    ) or 0
    return {'cart_items_count': total}
