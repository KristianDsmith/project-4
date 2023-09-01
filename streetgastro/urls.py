"""streetgastro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from booking import views 
from django.urls import include, path





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),  # Keep the name 'book'
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_view, name='menu'),
    path('menu_item_detail/<int:menu_item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('submit_rating/', views.submit_rating, name='submit_rating'),
]


    



