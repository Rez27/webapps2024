"""
URL configuration for webapps2024 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/webapps2024/')),
    path('webapps2024/', include('register.urls')),
    path('payapp/', include('payapp.urls')),
    path('conversion/', include('currency_conversion.urls')),
]
