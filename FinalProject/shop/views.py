from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm
from accounts.decorators import owner_or_employee_required

# Index View - Display featured products and categories
def index(request):
    featured_products = Product.objects.filter(available=True)[:8]  # Show top 8 featured products
    categories = Category.objects.filter(parent__isnull=True)  # Get top-level categories
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)  # Render homepage template

# Products View - List all available products with optional search and filters
def products(request):
    queryset = Product.objects.filter(available=True)
    search_query = request.GET.get('q')
    brand = request.GET.get('brand')
    size = request.GET.get('size')
    color = request.GET.get('color')
    
    if search_query:
        queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    if brand:
        queryset = queryset.filter(brand__iexact=brand)
    if size:
        queryset = queryset.filter(size__iexact=size)
    if color:
        queryset = queryset.filter(color__iexact=color)

    context = {'products': queryset}
    return render(request, 'shop/products.html', context)  # Render the product listing page with filtered products

# Product Detail View - Show individual product details and recommendations
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)  # Fetch the product
    recommendations = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]  # Related products
    context = {
        'product': product,
        'recommendations': recommendations,
    }
    return render(request, 'shop/product.html', context)  # Render the product detail page

# Category View - Show products within a specific category
def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products_in_category = Product.objects.filter(category=category, available=True)
    context = {
        'category': category,
        'products': products_in_category,
    }
    return render(request, 'shop/products.html', context)  # Render the category-specific product listing page

# Search View - Display search results based on the query
def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        available=True
    ) if query else Product.objects.none()
    
    context = {'products': results}
    return render(request, 'shop/products.html', context)  # Render search results in the products template

# Add Product View (only accessible by owners or employees)
@owner_or_employee_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new product to the database
            return redirect('shop:list_products')  # Redirect to the product list after adding
    else:
        form = ProductForm()
    return render(request, 'shop/employee/add.html', {'form': form})  # Render the add product form

# List Products View - List all products (only accessible by owners or employees)
@owner_or_employee_required
def list_products(request):
    products = Product.objects.all()  # Fetch all products in the system
    return render(request, 'shop/employee/list.html', {'products': products})  # Render the product list template

# Edit Product View (only accessible by owners or employees)
@owner_or_employee_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the edited product details
            return redirect('shop:list_products')  # Redirect to product list after editing
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/employee/edit.html', {'form': form, 'product': product})  # Render the product edit form

# Delete Product View (only accessible by owners or employees)
@owner_or_employee_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()  # Delete the product from the database
        return redirect('shop:list_products')  # Redirect to the product list after deletion
    return redirect('shop:list_products')  # If not POST, just redirect to the product list
