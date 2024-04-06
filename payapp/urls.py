from django.urls import path
from .views import main_page, admin_ui

urlpatterns = [
    path('main/', main_page, name='main_page'),
    path('admin_ui/', admin_ui, name='admin_ui'),
]
