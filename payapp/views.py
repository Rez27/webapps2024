from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm, PaymentForm, RequestForm
from .models import UserProfile, Transaction, Notification
from django.contrib.auth.models import User


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


def admin_ui(request):
    users = User.objects.all()
    user_profiles = UserProfile.objects.all()

    user_data = [(user, UserProfile.objects.get(user=user)) for user in users]

    context = {
        'user_data': user_data,
    }
    return render(request, 'payapp/admin_ui.html', context)
