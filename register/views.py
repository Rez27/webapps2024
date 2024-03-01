from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Implement user registration logic here
            return redirect('success_page')  # Redirect to a success page or login page
    else:
        form = RegistrationForm()

    return render(request, 'register/register.html', {'form': form})
