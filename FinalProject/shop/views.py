from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def index(request):
    trending_products = Product.objects.filter(available = True) [:6]
    categories = Category.objects.filter(parent=None)
    context = {
        'trending_products': trending_products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)

def products(request):
    products_list = Product.objects.filter(available=True)
    categories = Category.objects.filter(parent=None)
    context = {
        'products': products_list,
        'categories': categories,
    }
    return render(request, 'shop/products.html', context)

def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug, available = True)
    similar_products = product.get.similar_products()
    context ={
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'shop/product.html', context)

def checkout(request):
    return render(request, 'cart/checkout.html')

def cart(request):
    return render(request, 'cart/cart.html')