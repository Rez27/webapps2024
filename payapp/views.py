from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm
from .models import UserProfile


@login_required
def main_page(request):
    user = request.user
    try:
        user_profile = user.payapp_profile
        # If the user profile exists, update the balance
        user_profile_exists = True
    except UserProfile.DoesNotExist:
        # If the user profile doesn't exist, create a new profile with default balance
        user_profile = UserProfile.objects.create(user=user)
        user_profile_exists = False

    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if user_profile_exists:
                # If the user profile exists, update the existing balance
                user_profile.bal += amount
            else:
                # If the user profile doesn't exist, set the initial balance
                user_profile.bal = amount
            user_profile.save()
            return redirect('main')  # Redirect to a success page
    else:
        form = AddMoneyForm()
    currency = user_profile.currency
    if currency == 'GBP':
        cur = '£'
    elif currency == 'Euro':
        cur = '€'
    elif currency == 'Dollar':
        cur = '$'
    else:
        cur = "Error in getting currency"
    context = {
        'balance': user_profile.bal,
        'form': form,
        'cur': cur
    }
    return render(request, 'payapp/ui.html', context)