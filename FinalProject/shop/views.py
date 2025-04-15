from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product
from .forms import ProductForm
from accounts.decorators import owner_or_employee_required

def index(request):
    featured_products = Product.objects.filter(available = True)[:8]
    categories = Category.objects.filter(parent__isnull = True)
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)

def products(request):
    queryset = Product.objects.filter(available = True)
    search_query = request.GET.get('q')
    brand = request.GET.get('brand')
    size = request.GET.get('size')
    color = request.GET.get('color')
    if search_query:
        queryset = queryset.filter(Q(name__icontains = search_query) | Q(description__icontains = search_query))
    if brand:
        queryset = queryset.filter(brand__iexact = brand)
    if size:
        queryset = queryset.filter(size__iexact = size)
    if color:
        queryset = queryset.filter(color__iexact = color)
    context = {'products': queryset}
    return render(request, 'shop/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available = True)
    recommendations = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    context ={
        'product' : product,
        'recommendations': recommendations,
    }
    return render(request, 'shop/product.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products_in_category = Product.objects.filter(category = category, available=True)
    context = {
        'category': category,
        'products': products_in_category,
    }
    return render(request, 'shop/category.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(
        Q(name_icontains = query) | Q(description_icontains = query),
        available = True
    ) if query else Product.objects.none()

@owner_or_employee_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:modify_products')
    else:
        form = ProductForm()
    return render (request, 'shop/employee/add.html', {'form': form})

@owner_or_employee_required
def modify_products(reqeust):
    products = Product.objects.all()
    return render(reqeust, 'shop/employee/modify_products.html', {'products': products})

@owner_or_employee_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance = product)
        if form.is_valid():
            form.save()
            return redirect('shop:modify_products')
    else:
        form = ProductForm(instance = product)
    return render(request, 'shop/employee/edit.html', {'form' : form, 'product': product})

@owner_or_employee_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('shop:modify_products')
    return render(request, 'shop/employee/delete_confirm.html', {'product' : product})
