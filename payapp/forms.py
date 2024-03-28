from django import forms


class AddMoneyForm(forms.Form):
    amount = forms.IntegerField(label='Amount', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    addMoneyForm = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        if amount >= 1000:
            raise forms.ValidationError("Amount must be lower than 1000.")
        return amount


class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Pay Amount', required=True,
                                widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'}))
    first_name = forms.CharField(widget=forms.HiddenInput())
    last_name = forms.CharField(widget=forms.HiddenInput())
    currency_type = forms.CharField(widget=forms.HiddenInput())
    pay_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class RequestForm(forms.Form):
    requested_amount = forms.DecimalField(label='Request Amount', required=True,
                                widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'}))
    request_first_name = forms.CharField(widget=forms.HiddenInput())
    request_last_name = forms.CharField(widget=forms.HiddenInput())
    request_currency_type = forms.CharField(widget=forms.HiddenInput())
    request_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

