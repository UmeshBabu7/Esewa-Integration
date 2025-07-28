from django.urls import path
from .import views


urlpatterns = [
    path('', views.adminhome, name='admins'),

    # product
    path('productlist/', views.productlist, name='productlist'),
    path('addproduct/', views.addproduct, name='addproduct'),

     # category
    path('categorylist/', views.categorylist, name='categorylist'),
    path('addcategory/', views.addcategory, name='addcategory'),
]
