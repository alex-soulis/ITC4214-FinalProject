from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Review

@login_required
def submit_review(request):
    if request.method == 'POST' and request.is_ajax():
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        try:
            product = Product.objects.get(id=product_id, available = True)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'})
        
        review = Review.objects.create(
            product = product,
            user = request.user,
            rating = rating,
            comment = comment
        )
        return JsonResponse({'status': 'success', 'message': 'Review submitted.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
