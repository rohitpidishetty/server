"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bronchi_ulceration_detection import views
from ittacademy import views as itta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bud/', views.bud, name='Bronchi Ulceration Detection'),
    path('auth/', views.auth, name='AUTH'),
    path('pbm/', views.pbm, name='PBM'),
    path('success/', views.success, name='success'),
    path(f'user', itta.create_user, name='create_user')
      
]
