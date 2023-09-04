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
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.views import view_tasks 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_view, name='menu'),
    path('menu_item_detail/<int:menu_item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('submit_rating/', views.submit_rating, name='submit_rating'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('edit_confirmation/<int:booking_id>/', views.edit_confirmation, name='edit_confirmation'),
    path('confirm_cancel/<int:booking_id>/', views.confirm_cancel, name='confirm_cancel'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancellation_confirmation/', views.cancellation_confirmation, name='cancellation_confirmation'),
    path('task_manager/tasks/', view_tasks, name='task_manager_tasks'),

 


    



]





    






