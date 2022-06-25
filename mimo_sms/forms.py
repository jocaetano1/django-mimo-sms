from django import forms

from mimo_sms.models.credit import Activity
from mimo_sms.utils import charge_credits


class CreditForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('voucher',)

    def clean_voucher(self):
        voucher = self.cleaned_data.get('voucher')
        voucher = Activity.objects.filter(voucher=voucher)
        if voucher.exists():
            raise forms.ValidationError("Voucher is already registered.")
        if len(voucher) < 14:
            raise forms.ValidationError(
                'voucher', 'Voucher must be 14 characters long')
        return voucher

    def save(self, commit=True):
        super().save(commit=False)
        voucher = self.cleaned_data.get('voucher')
        instance = charge_credits(voucher)
        return instance
