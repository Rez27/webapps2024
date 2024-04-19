import requests
from requests.exceptions import RequestException
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm, PaymentForm, RequestForm, ShowTransactionsForm
from .models import Transaction, Notification
from register.models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse

# Thrift Time Service code
import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException
from datetime import datetime

timestamp_thrift = thriftpy.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


@login_required(login_url='/login/')
def main_page(request):
    user = request.user  # Logged in User
    username = request.user.username
    users = User.objects.exclude(pk=user.pk)  # Exclude the logged-in user
    user_profile, user_profile_exists = get_or_create_user_profile(user)
    addMoneyForm = AddMoneyForm()
    pay_form = PaymentForm()
    request_form = RequestForm()
    notifications = Notification.objects.filter(receiver=user)

    # To Show latest transactions
    try:
        received_transactions = list(reversed(Transaction.objects.filter(receiver=user.register_profile)))
        sent_transactions = list(reversed(Transaction.objects.filter(sender=user.register_profile)))
        print("This is received transactions", sent_transactions)
    except Exception as e:
        print("Didnt find transactions-", e)
        received_transactions = []
        sent_transactions = []
    if request.method == 'POST':
        # Add Money Logic
        if 'addMoneyForm' in request.POST:
            addMoneyForm = AddMoneyForm(request.POST)
            if addMoneyForm.is_valid():
                amount = addMoneyForm.cleaned_data['amount']
                if user_profile_exists:
                    user_profile.bal += amount
                else:
                    print("Money Not added")
                    user_profile.bal = amount
                user_profile.save()
                return redirect('main_page')
            else:
                print("Add money not valid")
                addMoneyForm = AddMoneyForm()

        # Pay Money To selected user logic
        elif 'pay_form' in request.POST:
            pay_form = PaymentForm(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                receiver_first_name = request.POST['first_name']
                receiver_last_name = request.POST['last_name']
                receiver_user_name = request.POST['user_name']
                try:
                    receiver_user = User.objects.get(first_name=receiver_first_name, last_name=receiver_last_name,
                                                     username=receiver_user_name)
                    receiver_profile = receiver_user.register_profile
                except:
                    print("Did not find receiver in app")
                    return redirect('main_page')
                sender_profile = request.user.register_profile

                # Perform currency conversion
                currency1 = user_profile.currency  # Get logged in user's (Sender's currency)
                currency2 = receiver_profile.currency  # Get receiver's currency
                print("This is currency1 currency2", currency1, currency2)
                converted_amount = convert_currency(currency1, currency2, amount)
                if converted_amount is None:
                    # Handle currency conversion error
                    context = {
                        'conversion_error': 'Failed to convert currency.'}
                    print("Something wrong in amount conversion")
                    return render(request, 'payapp/ui.html', context)
                try:
                    client = make_client(Timestamp, '127.0.0.1', 9090)
                    timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
                    print("This is time", timestamp)
                    if sender_profile.bal <= 0 or float("{:.2f}".format(amount)) > sender_profile.bal:
                        print("Not enough user balance")
                        error_message = "You've got low balance. Please Add Money to your account before carrying out any transactions."
                        context = {
                            'user_balance': user_profile.bal,
                            'user_currency': user_profile.currency,
                            'addMoneyForm': addMoneyForm,
                            'pay_form': pay_form,
                            'request_form': request_form,
                            'username': username,
                            'users': users,
                            'notifications': notifications,
                            'received_transactions': received_transactions,
                            'sent_transactions': sent_transactions,
                            'error_message': error_message
                        }
                        return render(request, 'payapp/ui.html', context)
                    sender_profile.bal -= float("{:.2f}".format(amount))
                    sender_profile.save()

                    # Add amount to receiver
                    receiver_profile.bal += float("{:.2f}".format(converted_amount))
                    receiver_profile.save()
                    sent_currency = currency1
                    received_currency = currency2
                    # Create transaction record
                    transaction = Transaction.objects.create(sender=sender_profile, receiver=receiver_profile,
                                                             amount=amount, sent_currency=sent_currency,
                                                             received_currency=received_currency, timestamp=timestamp)
                    transaction.save()
                    PaymentForm()
                    return redirect('main_page')  # Redirect to a success page
                except TException as e:
                    print("TimeStamp Server not Runnning. Issue-", e)
                    return redirect('main_page')
            else:
                print("Pay Form not valid")
                pay_form = PaymentForm()

        # Request Money form
        elif 'request_form' in request.POST:
            request_form = RequestForm(request.POST)
            if request_form.is_valid():
                amount = request_form.cleaned_data['requested_amount']
                currency_amount = request_form.cleaned_data['request_currency_type']
                request_first_name = request.POST['request_first_name']
                request_last_name = request.POST['request_last_name']
                receiver_user_name = request.POST['request_user_name']
                try:
                    Notification.objects.create(
                        receiver=User.objects.get(first_name=request_first_name, last_name=request_last_name,
                                                  username=receiver_user_name),
                        requester=request.user,
                        amount=amount,
                    )
                except:
                    print("Notification not created for money request")
                    return redirect('main_page')

                sender_profile = request.user.register_profile
                RequestForm()
                return redirect('main_page')  # Redirect to a success page
            else:
                print("Request form not valid")
                request_form = RequestForm()

        # Accept Notification
        elif 'accept_notification' in request.POST:
            requester = request.POST['requester_username']
            requested_amount = request.POST['requested_amount']

            try:
                sender_user = User.objects.get(username=requester)
                sender_profile = sender_user.register_profile
            except User.DoesNotExist:
                print("Sender profile not found in accept Notification")
                return redirect('main_page')
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
        print("Something wrong with request type")
        addMoneyForm = AddMoneyForm()
        pay_form = PaymentForm()
        request_form = RequestForm()

    context = {
        'user_balance': user_profile.bal,
        'user_currency': user_profile.currency,
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
        user_profile = user.register_profile
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
        # Generate the URL for the currency conversion endpoint
        url = f"http://127.0.0.1:8000/conversion/{currency1}/{currency2}/{amount}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            conversion_rate = data['conversion_rate']  # NOt returned for now. Can use this to show the conversion rate
            converted_amount = data['converted_amount']
            return converted_amount
        else:
            return None, None
    except requests.RequestException:
        return None, None


@login_required(login_url='/login/')
def admin_ui(request):
    if request.user.userprofile.is_superuser:
        users = User.objects.all()
        user_data = [(user, UserProfile.objects.get(user=user)) for user in users]
        transactions_sent = None
        transactions_received = None
        show_transactions_form = ShowTransactionsForm()
        transactions_sent = []  # Set to empty list
        transactions_received = []  # Set to empty list

        if request.method == 'POST':
            if 'show_transactions' in request.POST:
                show_transactions_form = ShowTransactionsForm(request.POST)
                if show_transactions_form.is_valid():
                    first_name = show_transactions_form.cleaned_data['show_trans_first_name']
                    last_name = show_transactions_form.cleaned_data['show_trans_last_name']
                    username = show_transactions_form.cleaned_data['show_trans_user_name']

                    print("This is ", first_name, last_name)
                    try:
                        user = User.objects.get(first_name=first_name,
                                                last_name=last_name,
                                                username=username)  # Here try to get the user selected for Show Transaction button
                        user_profile = UserProfile.objects.get(user=user)
                        transactions_sent = list(reversed(Transaction.objects.filter(sender=user_profile)))
                        transactions_received = list(reversed(Transaction.objects.filter(receiver=user_profile)))
                        print("THis is transactions_sent", transactions_sent)
                    except (User.DoesNotExist, UserProfile.DoesNotExist):
                        print("Error in getting user data")
                        transactions = None
                else:
                    print("Show Transaction form not valid")
                    print(show_transactions_form.errors)
            else:
                print("Wrong in form")
        else:
            print("Request method not valid")
            show_transactions_form = ShowTransactionsForm()
            transactions_sent = []  # Set to empty list
            transactions_received = []  # Set to empty list

        context = {
            'users': users,
            'user_data': user_data,
            'show_transactions_form': show_transactions_form,
            'transactions_sent': transactions_sent,
            'transactions_received': transactions_received,
        }
        return render(request, 'payapp/admin_ui.html', context)
    else:
        return redirect('login')
