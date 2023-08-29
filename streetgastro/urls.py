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
from booking import views as booking_views
from booking.views import task_list, task_detail
from booking.views import staff_tasks




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('restaurant_hours/', views.restaurant_hours, name='restaurant_hours'),
    path('book/', views.book, name='book'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_view, name='menu'),
    path('update_reservation/<int:pk>/', views.ReservationUpdateView.as_view(), name='update_reservation'),
    path('cancel_reservation/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('menu_item_detail/<int:menu_item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('submit_rating/', views.submit_rating, name='submit_rating'),
    path('table_status/', views.table_status, name='table_status'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('staff_tasks/', views.staff_tasks, name='staff_tasks'),
    path('reservation_detail/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('staff_login/', views.staff_login_view, name='staff_login'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
]


    



