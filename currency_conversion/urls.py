from django.urls import path
from .views import CurrencyConversion

urlpatterns = [
    path('<str:currency1>/<str:currency2>/<str:amount>/', CurrencyConversion.as_view(), name='currency_conversion'),
]