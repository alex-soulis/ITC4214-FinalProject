from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Review
from django.views.decorators.http import require_POST

@login_required
@require_POST
def submit_review(request):
    product_id = request.POST.get('product_id')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '')
    product = get_object_or_404(Product, id = product_id, available = True)
    review = Review.objects.create(
        product = product,
        user = request.user,
        rating = rating,
        comment = comment
    )
    return JsonResponse({'status': 'success', 'message': 'Review submitted.'})

