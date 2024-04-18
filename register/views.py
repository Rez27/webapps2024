from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from .models import UserProfile
from payapp.views import admin_ui


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Register view success")
            return redirect('login')
        else:
            print("Register view Fail1")
            return render(request, 'register/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        print("Register view Fail2")
        return render(request, 'register/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_superuser = form.cleaned_data['is_superuser']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if is_superuser and user.userprofile.is_superuser:
                    # Redirect the superuser to the admin UI page
                    return redirect('admin_ui')
                else:
                    return redirect('main')
        else:
            return render(request, 'register/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})
