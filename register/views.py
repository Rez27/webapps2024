from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegistrationForm


from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Your custom validation logic
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Example: Check if the username is already taken
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')

            # Example: Check if the email is already registered
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')

            # If there are no validation errors, proceed with user registration
            if not form.errors:

                return redirect('success_page')

    else:
        form = RegistrationForm()

    return render(request, 'register/register.html', {'form': form})


def success_page(request):
    return render(request, 'register/success_page.html')
