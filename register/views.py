from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserCreationForm, LoginForm


def main(request):
    return render(request, 'register/ui.html')
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)

            if user:
                    login(request, user)
                    main_page_url = reverse('payapp:main_page')
                    # Redirect to the main page
                    return redirect(main_page_url)
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
