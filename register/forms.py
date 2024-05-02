from django import forms

import payapp.views
from .validations import user_email_check, username_check
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


def email_val(email):
    if user_email_check(email=email):
        raise forms.ValidationError("User already exists")

#User Registratin form consisting of basic fields along with currency choices
class UserRegistrationForm(UserCreationForm):
    currency_choices = [
        ('GBP', 'GBP'),
        ('EUR', 'Euro'),
        ('USD', 'Dollar')
    ]
    currency = forms.ChoiceField(choices=currency_choices)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['currency'].required = True

#Save Function to save form into the models
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.currency = self.cleaned_data['currency']
        user_profile.email = self.cleaned_data['email']
        baseline_amount = 1000
        currency1 = 'GBP'
        currency2 = user_profile.currency
        converted_acc_bal = payapp.views.convert_currency(currency1, currency2, baseline_amount)
        user_profile.bal = converted_acc_bal
        user_profile.save()
        return user
#Login Form for user along side is_superuser field for checking admin login
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    is_superuser = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True


#Admmin Registration form similar to user registration form but only restricted to admin. Here is_superuser is set to True by default on save
class AdminRegistrationForm(UserCreationForm):
    currency_choices = [
        ('GBP', 'GBP'),
        ('EUR', 'Euro'),
        ('USD', 'Dollar')
    ]
    currency = forms.ChoiceField(choices=currency_choices)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency']

    def __init__(self, *args, **kwargs):
        super(AdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['currency'].required = True

    def save(self, commit=True):
        user = super(AdminRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = user.is_superuser = True
        user.is_superuser = True  # Set is_superuser to True for the User model
        if commit:
            user.save()
            # Create or get UserProfile and set is_superuser to True
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.currency = self.cleaned_data['currency']
            user_profile.email = self.cleaned_data['email']
            baseline_amount = 1000
            currency1 = 'GBP'
            currency2 = user_profile.currency
            converted_acc_bal = payapp.views.convert_currency(currency1, currency2, baseline_amount)
            user_profile.bal = converted_acc_bal
            user_profile.is_superuser = True
            user_profile.save()

        return user



