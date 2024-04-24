from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


#Class CurrencyConversion which is an APIView subclass
class CurrencyConversion(APIView):

    # Method to retrieve conversion rate between two currencies
    def get_conversion_rate(self, currency1, currency2):
        # Dictionary containing conversion rates between different currencies
        conversion_rates = {
            'USD': {'EUR': 0.85, 'GBP': 0.73, 'USD':1},
            'EUR': {'USD': 1.18, 'GBP': 0.86, 'EUR':1},
            'GBP': {'USD': 1.38, 'EUR': 1.16, 'GBP':1},
        }
        # Return the conversion rate if available, otherwise return None
        return conversion_rates.get(currency1, {}).get(currency2)

    # Define a method to handle GET requests
    def get(self, request, currency1, currency2, amount):
        # Retrieve conversion rate between the specified currencies
        conversion_rate = self.get_conversion_rate(currency1, currency2)

        # If conversion rate is not available, return an error response with status code 404
        if conversion_rate is None:
            return Response({'error': 'Conversion rate not available'}, status=status.HTTP_404_NOT_FOUND)

        # Perform currency conversion
        try:
            # Convert the amount from string to float and perform conversion calculation
            converted_amount = float(amount) * conversion_rate
            # Prepare the response data with conversion rate and converted amount
            response_data = {'conversion_rate': conversion_rate, 'converted_amount': converted_amount}
            # Return a success response with the converted data and status code 200
            return Response(response_data, status=status.HTTP_200_OK)
        # Handle the case where an invalid amount is provided
        except ValueError:
            # Return an error response with status code 400 indicating bad request
            return Response({'error': 'Invalid amount provided'}, status=status.HTTP_400_BAD_REQUEST)
