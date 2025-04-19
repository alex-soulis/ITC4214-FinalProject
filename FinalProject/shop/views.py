from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm
from accounts.decorators import owner_or_employee_required

# Index View - Display featured products and categories
def index(request):
    trending_products = Product.objects.filter(available=True).order_by('?')[:6]  # Get random products for trending section
    categories = Category.objects.filter(parent__isnull=True)  # Get top-level categories
    context = {
        'trending_products': trending_products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)  # Render homepage template

# Products View - List all available products with optional search and filters
def products(request):
    # 1) Base queryset of available products
    queryset = Product.objects.filter(available=True)

    # 2) Read all filters from GET
    q            = request.GET.get('q', '')
    category_ids = request.GET.getlist('category')
    brand_list   = request.GET.getlist('brand')
    size_list    = request.GET.getlist('size')
    color_list   = request.GET.getlist('color')

    # 3) Apply search / category / brand filters
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )
    if category_ids:
        queryset = queryset.filter(category__id__in=category_ids)
    if brand_list:
        queryset = queryset.filter(brand__in=brand_list)
    # 4) Apply size & color filters as substring matches
    if size_list:
        size_q = Q()
        for s in size_list:
            size_q |= Q(size__icontains=s)
        queryset = queryset.filter(size_q)
    if color_list:
        color_q = Q()
        for c in color_list:
            color_q |= Q(color__icontains=c)
        queryset = queryset.filter(color_q)

    # 5) Build master list of all size‑tokens (splitting the comma field)
    size_tokens = set()
    for p in Product.objects.filter(available=True):
        raw = p.size or ""
        for tok in raw.split(","):
            tok = tok.strip()
            if tok:
                size_tokens.add(tok)

    # 6) Define your apparel vs shoe size lists
    apparel_order = ["S", "M", "L", "XL"]
    sizes_apparel = [s for s in apparel_order if s in size_tokens]
    # numeric shoe sizes
    shoe_sizes = sorted(
    (tok for tok in size_tokens if tok.isdigit()),
    key=lambda x: int(x)
)

    # 7) Prepare the other filter lists
    all_categories = Category.objects.filter(parent__isnull=True).order_by("name")
    all_brands     = (
        Product.objects
               .order_by("brand")
               .values_list("brand", flat=True)
               .distinct()
    )
    all_colors     = (
        Product.objects
               .order_by("color")
               .values_list("color", flat=True)
               .distinct()
    )

    # 8) Find the Shoes category ID (for Alpine toggling)
    shoe_cat = Category.objects.filter(name__iexact="shoes").first()

    # 9) Assemble context, including your two new lists
    context = {
        "products":         queryset,
        "categories":       all_categories,
        "brands":           all_brands,
        "colors":           all_colors,
        # master sizes list (unused if you always use sizes_apparel/shoe_sizes)
        "sizes":            sizes_apparel + shoe_sizes,
        # what’s currently checked
        "selected": {
            "q":           q,
            "categories":  list(map(int, category_ids)),
            "brands":      brand_list,
            "sizes":       size_list,
            "colors":      color_list,
        },
        # Alpine helpers
        "shoe_category_id": shoe_cat.id if shoe_cat else None,
        "sizes_apparel":    sizes_apparel,
        "shoe_sizes":       shoe_sizes,
    }

    return render(request, "shop/products.html", context)


# Product Detail View - Show individual product details and recommendations
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    recommendations = (
        Product.objects
               .filter(category=product.category, available=True)
               .exclude(id=product.id)[:4]
    )

    # 1) Images — if you only have the single ImageField on Product:
    images = []
    if product.image:
        images.append(product.image)

    # 2) Colors — if your Product.color is a comma‑separated string:
    raw = product.color or ""
    color_names = [c.strip() for c in raw.split(",") if c.strip()]
    # Turn each into an object with value/bg_class for your template:
    colors = [
        {
            "value": name, 
            # tailwind bg class—lowercase, no spaces, adjust if your naming differs
            "bg_class": f"bg-{name.lower().replace(' ', '-')}-500"
        }
        for name in color_names
    ]

    # 3) Sizes — using the M2M Size model you already migrated in 0003:
    raw = product.size or ""
    sizes = [s.strip() for s in raw.split(",") if s.strip()]

    context = {
        "product": product,
        "recommendations": recommendations,
        "images": images,
        "colors": colors,
        "sizes": sizes,
    }
    return render(request, "shop/product.html", context)
  # Render the product detail page

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
    return render(request, 'shop/employees/add.html', {'form': form})  # Render the add product form

# List Products View - List all products (only accessible by owners or employees)
@owner_or_employee_required
def list_products(request):
    products = Product.objects.all()  # Fetch all products in the system
    return render(request, 'shop/employees/list.html', {'products': products})  # Render the product list template

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
    return render(request, 'shop/employees/edit.html', {'form': form, 'product': product})  # Render the product edit form

# Delete Product View (only accessible by owners or employees)
@owner_or_employee_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()  # Delete the product from the database
        return redirect('shop:list_products')  # Redirect to the product list after deletion
    return redirect('shop:list_products')  # If not POST, just redirect to the product list
