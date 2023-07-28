from django.shortcuts import render
from .models import MenuItem


def browse_menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})


def homepage(request):
    return render(request, 'homepage.html')


def make_reservation(request):
    return render(request, 'make_reservation.html')
