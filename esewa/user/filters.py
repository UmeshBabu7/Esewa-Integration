import django_filters
from django_filters import CharFilter
from django import forms
from product.models import *

class ProductFilter(django_filters.FilterSet):
    product_name_contains = CharFilter(
        field_name='product_name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search products…',
                'class': 'border border-gray-300 rounded px-3 py-2 w-72'
            }
        ),
    )
    class Meta:
        model=Product
        fields=''
        exclude=['product_price','description','quantity','image','category','created_at','updated_at']