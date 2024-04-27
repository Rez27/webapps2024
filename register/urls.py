from django.urls import path
from .views import register, user_login, register_admin
from payapp.views import main_page

urlpatterns = [
    path('', register, name='register'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('main/', main_page, name='main'),
    path('register_admin/', register_admin, name='register_admin')
]
