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

    # update and delete product
    path('updateproduct/<int:product_id>/', views.updateproduct, name='updateproduct'),
    path('deleteproduct/<int:product_id>/', views.deleteproduct, name='deleteproduct'),

    # update and delete category
    path('updatecategory/<int:category_id>/', views.updatecategory, name='updatecategory'),
    path('deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory')
]
