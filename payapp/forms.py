from django import forms


class AddMoneyForm(forms.Form):
    amount = forms.IntegerField(label='Amount', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        if amount >= 1000:
            raise forms.ValidationError("Amount must be lower than 1000.")
        return amount
