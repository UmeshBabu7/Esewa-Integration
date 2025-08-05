from django.urls import path
from .import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('productpage/', views.productpage, name='productpage'),
    
    # product detail
    path('productdetail/<int:product_id>/', views.productdetail, name='productdetail'),

    # user authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
