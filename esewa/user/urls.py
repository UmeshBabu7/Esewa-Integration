from django.urls import path
from .import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('productpage/', views.productpage, name='productpage'),
    path('productdetail/<int:product_id>/', views.productdetail, name='productdetail')
]
