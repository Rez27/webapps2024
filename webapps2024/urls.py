"""
URL configuration for webapps2024 project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapps2024/', include('register.urls')),
    path('payapp/', include('payapp.urls')),
    path('conversion/', include('currency_conversion.urls')),

]
