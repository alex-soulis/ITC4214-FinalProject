# cart/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import Cart, CartItem

# Internal helper: fetch-or-create the right Cart
def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

def view_cart(request):
    cart = _get_cart(request)
    items = CartItem.objects.filter(cart=cart) if cart else []
    # Compute summary
    subtotal = sum(item.product.price * item.quantity for item in items)
    shipping = Decimal('00.00')                   # your logic here
    total    = subtotal + shipping

    context = {
        'cart_items': items,
        'order': {
            'items':    items,
            'subtotal': subtotal,
            'shipping': shipping,
            'total':    total,
        },
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = _get_cart(request)
    # grab the customer’s choices
    size  = request.POST.get('size')
    color = request.POST.get('color')

    # grouping by product+size+color so different selections get separate line‑items
    item, created = CartItem.objects.get_or_create(
         cart=cart,
         product=product,
         size=size,
         color=color,
     )
    if not created:
        item.quantity += 1
        item.save()
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart'))

@require_POST
def update_cart(request):
    cart = _get_cart(request)
    for key, val in request.POST.items():
        if key.startswith('quantity_'):
            item_id = key.split('_', 1)[1]
            try:
                qty = int(val)
                item = CartItem.objects.get(cart=cart, id=item_id)
            except (ValueError, CartItem.DoesNotExist):
                continue
            if qty > 0:
                item.quantity = qty
                item.save()
            else:
                item.delete()
    return redirect('cart:cart')

@require_POST
def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, cart=cart, id=item_id)
    item.delete()
    return redirect('cart:cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    subtotal = sum(item.product.price * item.quantity for item in items)
    shipping = Decimal('00.00')
    total    = subtotal + shipping
    order = {
        'items':    items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total':    total,
    }

    if request.method == 'POST':
        cart.items.all().delete()
        return redirect('accounts:dashboard')

    return render(request, 'cart/checkout.html', {'order': order})
