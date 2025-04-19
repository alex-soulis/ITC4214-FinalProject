# shop/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'brand',
            'color',
            'size',
            'image',
            'stock',
            'available',
            'category',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
                'rows': 3,
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
                'placeholder': 'Brand name'
            }),
            'color': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
                'placeholder': 'Color'
            }),
            'size': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
                'placeholder': 'Enter size (if applicable)'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600',
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded',
            }),
            'category': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-600 focus:ring-indigo-600'
            }),
        }