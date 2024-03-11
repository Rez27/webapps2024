from django.urls import path
from .views import register
from payapp.views import main_page

urlpatterns = [
    path('register/', register, name='register'),
    path('main/', main_page, name='main'),

]
