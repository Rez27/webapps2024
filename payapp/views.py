from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm, PaymentForm, RequestForm
from .models import UserProfile, Transaction, Notification
from django.contrib.auth.models import User


# @login_required
# def main_page(request):
#     user = request.user
#     username = request.user.username
#     users = User.objects.all() #All Users
#     # Excluding the currently authenticated user
#     logged_in_user = request.user
#     users = users.exclude(pk=logged_in_user.pk)
#
#     try:
#         user_profile = user.payapp_profile
#         # If the user profile exists, update the balance
#         user_profile_exists = True
#     except UserProfile.DoesNotExist:
#         # If the user profile doesn't exist, create a new profile with default balance
#         user_profile = UserProfile.objects.create(user=user)
#         user_profile_exists = False
#
#     if request.method == 'POST':
#         form = AddMoneyForm(request.POST)
#         pay_form = PaymentForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             if user_profile_exists:
#                 # If the user profile exists, update the existing balance
#                 user_profile.bal += amount
#             else:
#                 # If the user profile doesn't exist, set the initial balance
#                 user_profile.bal = amount
#             user_profile.save()
#             return redirect('main')  # Redirect to a success page
#
#         elif pay_form.is_valid():
#             amount = pay_form.cleaned_data['amount']
#             # receiver_id = request.POST.get('receiver_id')
#             receiver_profile = UserProfile.objects.get(user__id=receiver_id)
#             sender_profile = request.user.payapp_profile
#
#             # Deduct amount from sender
#             sender_profile.bal -= amount
#             sender_profile.save()
#
#             # Add amount to receiver
#             receiver_profile.bal += amount
#             receiver_profile.save()
#
#             # Create transaction record
#             transaction = Transaction.objects.create(sender=sender_profile, receiver=receiver_profile, amount=amount)
#             transaction.save()
#
#             return redirect('main')  # Redirect to a success page
#     else:
#         form = AddMoneyForm()
#
#     currency = user_profile.currency
#
#     context = {
#         'balance': user_profile.bal,
#         'form': form,
#         'cur': get_currency_symbol(currency),
#         'username': username,
#         'users': users
#     }
#     return render(request, 'payapp/ui.html', context)

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
                    # If the user profile exists, update the existing balance
                    user_profile.bal += amount
                else:
                    # If the user profile doesn't exist, set the initial balance
                    user_profile.bal = amount
                user_profile.save()
                return redirect('main_page')  # Redirect to a success page
        # Pay Money Form
        elif 'pay_form' in request.POST:
            pay_form = PaymentForm(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                receiver_first_name = request.POST['first_name']
                receiver_last_name = request.POST['last_name']
                print("This is user", receiver_first_name, receiver_last_name)
                try:
                    receiver_user = User.objects.get(first_name=receiver_first_name, last_name=receiver_last_name)
                    receiver_profile = receiver_user.payapp_profile
                except:
                    print("No User")
                    return redirect('main_page')

                sender_profile = request.user.payapp_profile

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

    currency = user_profile.currency
    cur = get_currency_symbol(currency)

    # To Show latest transactions
    received_transactions = Transaction.objects.filter(receiver=user.payapp_profile)
    sent_transactions = Transaction.objects.filter(sender=user.payapp_profile)

    context = {
        'balance': user_profile.bal,
        'addMoneyForm': addMoneyForm,
        'pay_form': pay_form,
        'request_form': request_form,
        'cur': cur,
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
