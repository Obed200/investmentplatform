from django import forms

from .models import Deposit, Withdrawal


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["plan", "proof"]

    def __init__(self, *args, **kwargs):
        plans = kwargs.pop("plans", None)
        super().__init__(*args, **kwargs)
        if plans is not None:
            self.fields["plan"].queryset = plans

    def clean_proof(self):
        pic = self.cleaned_data.get('proof')
        if not pic:
            raise forms.ValidationError('Payment proof is required')
        if pic.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Proof image must be <= 5MB')
        if not pic.content_type.startswith('image/'):
            raise forms.ValidationError('Invalid image file')
        return pic


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount", "phone_number"]
