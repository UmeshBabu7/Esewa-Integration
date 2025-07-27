from django.urls import path
from .import views


urlpatterns = [
    path('', views.adminhome, name='admins'),
    path('productlist/', views.productlist, name='productlist')
]
