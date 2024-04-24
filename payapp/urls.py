from django.urls import path
from .views import main_page, admin_ui
from django.contrib.auth import views as auth_views
from register.views import register, login



urlpatterns = [
    path('main/', main_page, name='main_page'),
    path('admin_ui/', admin_ui, name='admin_ui'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]