import requests
from requests.exceptions import RequestException
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm, PaymentForm, RequestForm, ShowTransactionsForm
from .models import UserProfile, Transaction, Notification
from django.contrib.auth.models import User
from django.urls import reverse


@login_required
def main_page(request):
    user = request.user  # Logged in User
    username = request.user.username
    users = User.objects.exclude(pk=user.pk)  # Exclude the logged-in user
    user_profile, user_profile_exists = get_or_create_user_profile(user)
    addMoneyForm = AddMoneyForm()
    pay_form = PaymentForm()
    request_form = RequestForm()
    notifications = Notification.objects.filter(receiver=user)

    if request.method == 'POST':
        # Add Money Logic
        if 'addMoneyForm' in request.POST:
            print("In add money")
            addMoneyForm = AddMoneyForm(request.POST)
            if addMoneyForm.is_valid():
                amount = addMoneyForm.cleaned_data['amount']
                if user_profile_exists:
                    user_profile.bal += amount
                else:
                    user_profile.bal = amount
                user_profile.save()
                return redirect('main_page')
            else:
                addMoneyForm = AddMoneyForm()

        # Pay Money Form
        elif 'pay_form' in request.POST:
            pay_form = PaymentForm(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                receiver_first_name = request.POST['first_name']
                receiver_last_name = request.POST['last_name']
                # print("This is user", receiver_first_name, receiver_last_name)
                try:
                    receiver_user = User.objects.get(first_name=receiver_first_name, last_name=receiver_last_name)
                    receiver_profile = receiver_user.payapp_profile
                except:
                    print("No User")
                    return redirect('main_page')

                sender_profile = request.user.payapp_profile
                # Perform currency conversion
                currency1 = user_profile.currency  # Get logged in user's (Sender's currency)
                currency2 = receiver_profile.currency  # Get receiver's currency
                converted_amount = convert_currency(currency1, currency2, amount)
                print("This is converted_amount", converted_amount)
                if converted_amount is None:
                    # Handle currency conversion error
                    context = {
                        'conversion_error': 'Failed to convert currency.'}
                    return render(request, 'payapp/ui.html', context)
                # Deduct amount from sender
                sender_profile.bal -= amount
                sender_profile.save()

                # Add amount to receiver
                receiver_profile.bal += amount
                receiver_profile.save()

                # Create transaction record
                transaction = Transaction.objects.create(sender=sender_profile, receiver=receiver_profile,
                                                         amount=amount)
                transaction.save()

                return redirect('main_page')  # Redirect to a success page
            else:
                pay_form = PaymentForm()

        # Request Money form
        elif 'request_form' in request.POST:
            request_form = RequestForm(request.POST)
            if request_form.is_valid():
                print("In valid request_form")
                amount = request_form.cleaned_data['requested_amount']
                currency_amount = request_form.cleaned_data['request_currency_type']
                request_first_name = request.POST['request_first_name']
                request_last_name = request.POST['request_last_name']
                print("This is user to request", request_first_name, request_last_name, "Requested by", request.user,
                      "And ammount is", amount)
                try:
                    Notification.objects.create(
                        receiver=User.objects.get(first_name=request_first_name, last_name=request_last_name),
                        requester=request.user,
                        amount=amount,
                    )
                except:
                    print("Notification not created")
                    return redirect('main_page')

                sender_profile = request.user.payapp_profile

                return redirect('main_page')  # Redirect to a success page
            else:
                request_form = RequestForm()

        # Accept Notification
        elif 'accept_notification' in request.POST:
            requester = request.POST['requester_username']
            requested_amount = request.POST['requested_amount']

            try:
                sender_user = User.objects.get(username=requester)
                sender_profile = sender_user.payapp_profile
            except User.DoesNotExist:
                return redirect('main_page')
            print("This is sender_profile.bal", type(sender_profile.bal))
            sender_profile.bal = float(sender_profile.bal)
            requested_amount = float(requested_amount)

            sender_profile.bal += requested_amount
            sender_profile.save()

            user_profile.bal -= requested_amount
            user_profile.save()

            notification_id = request.POST['notification_id']
            notification = get_object_or_404(Notification, pk=notification_id)
            # Mark the notification as accepted
            notification.is_accepted = True
            notification.save()
            # Delete the notification after all transactions are successful
            notification.delete()

            return redirect('main_page')
    else:
        addMoneyForm = AddMoneyForm()
        pay_form = PaymentForm()
        request_form = RequestForm()

    # To Show latest transactions
    received_transactions = list(reversed(Transaction.objects.filter(receiver=user.payapp_profile)))
    sent_transactions = Transaction.objects.filter(sender=user.payapp_profile)

    context = {
        'balance': user_profile.bal,
        'addMoneyForm': addMoneyForm,
        'pay_form': pay_form,
        'request_form': request_form,
        'username': username,
        'users': users,
        'notifications': notifications,
        'received_transactions': received_transactions,
        'sent_transactions': sent_transactions
    }
    return render(request, 'payapp/ui.html', context)


def get_or_create_user_profile(user):
    try:
        user_profile = user.payapp_profile
        user_profile_exists = True
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
        user_profile_exists = False
    return user_profile, user_profile_exists


def get_currency_symbol(currency):
    if currency == 'GBP':
        return '£'
    elif currency == 'Euro':
        return '€'
    elif currency == 'Dollar':
        return '$'
    else:
        return "Error in getting currency"


def convert_currency(currency1, currency2, amount):
    try:
        print("This is currency 1", currency1, "and this is currency 2", currency2)
        # Generate the URL for the currency conversion endpoint
        url = f"http://127.0.0.1:8000/conversion/{currency1}/{currency2}/{amount}/"
        response = requests.get(url)
        print(response.status_code)
        print(response.json())
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response to get the conversion rate and converted amount
            data = response.json()
            conversion_rate = data['conversion_rate']
            converted_amount = data['converted_amount']
            return conversion_rate, converted_amount
        else:
            # Handle the case where the request was not successful (e.g., invalid currencies)
            return None, None
    except requests.RequestException:
        # Handle exceptions related to network errors or invalid URLs
        return None, None


def admin_ui(request):
    users = User.objects.all()
    user_data = [(user, UserProfile.objects.get(user=user)) for user in users]
    transactions_sent = None
    transactions_received = None
    if request.method == 'POST':
        show_transactions_form = ShowTransactionsForm(request.POST)
        if show_transactions_form.is_valid():
            first_name = show_transactions_form.cleaned_data['first_name']
            last_name = show_transactions_form.cleaned_data['last_name']
            try:
                user = User.objects.get(first_name=first_name,
                                        last_name=last_name)  # Here try to get the user selected for Show Transaction button
                user_profile = UserProfile.objects.get(user=user)
                print("This is user_profile", user_profile)
                transactions_sent = Transaction.objects.filter(sender=user_profile)
                transactions_received = Transaction.objects.filter(receiver=user_profile)
                # transactions = transactions_sent | transactions_received
                print("These are transactions for user", user_profile, "which is", transactions_sent)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                transactions = None

    else:
        show_transactions_form = ShowTransactionsForm()

    context = {
        'user_data': user_data,
        'show_transactions_form': show_transactions_form,
        'transactions_sent': transactions_sent,
        'transactions_received': transactions_received,
    }
    return render(request, 'payapp/admin_ui.html', context)
