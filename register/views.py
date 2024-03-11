from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            return render(request, 'register/login.html', {'form': form})
    else:
        return render(request, 'register/login.html', {'form': UserRegistrationForm()})

# def user_signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('register')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register/login.html', {'form': form})
#
#
# # login page
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('main')
#     else:
#         form = LoginForm()
#     return render(request, 'register/register.html', {'form': form})
#
#
# # logout page
# def user_logout(request):
#     logout(request)
#     return redirect('login')

# def register(request):
#     return render(request, 'register/login.html')
