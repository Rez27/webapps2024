from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CurrencyConversion(APIView):
    def get_conversion_rate(self, currency1, currency2):
        # Placeholder implementation to fetch conversion rate
        # Replace this with your actual implementation to fetch conversion rates
        conversion_rates = {
            'USD': {'EUR': 0.85, 'GBP': 0.73, 'USD':1},
            'EUR': {'USD': 1.18, 'GBP': 0.86, 'EUR':1},
            'GBP': {'USD': 1.38, 'EUR': 1.16, 'GBP':1},
        }
        return conversion_rates.get(currency1, {}).get(currency2)

    def get(self, request, currency1, currency2, amount):
        # Check if conversion rate is available
        conversion_rate = self.get_conversion_rate(currency1, currency2)
        if conversion_rate is None:
            return Response({'error': 'Conversion rate not available'}, status=status.HTTP_404_NOT_FOUND)

        # Perform currency conversion
        try:
            converted_amount = float(amount) * conversion_rate
            response_data = {'conversion_rate': conversion_rate, 'converted_amount': converted_amount}
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid amount provided'}, status=status.HTTP_400_BAD_REQUEST)
