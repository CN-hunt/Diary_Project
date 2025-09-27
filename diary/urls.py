"""
URL configuration for diary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from Web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/sendemail/', views.sendemail, name='sendemail'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('image/code/', views.image_code, name='image_code'),

    # 日记本操作
    path('notebook/add', views.notebook_add, name='notebook_add'),
    path('notebook/<int:nid>/del/', views.notebook_del, name='notebook_del'),
    path('notebook/content/<int:nid>/show/', views.notebook_content_show, name='notebook_content_show'),

]
