from django.urls import path
from .views import register_user,success_page

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('success/', success_page, name='success_page'),

]
