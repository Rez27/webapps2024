from django.urls import path
from .views import main_page

urlpatterns = [
    path('main/', main_page, name='main_page'),
]
