
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('admins/', include('adminpage.urls')),
    path('', include('user.urls')),
]
