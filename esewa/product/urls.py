from django.urls import path
from .import views


urlpatterns = [
    path('product/',views.product),
    path('', views.home, name='home'),
    path('productpage/', views.productpage, name='productpage')
]
