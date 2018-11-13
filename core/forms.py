from django import forms

from accounts.models import Deck


class DeckForm(forms.ModelForm):
    name = forms.CharField(max_length=120, required=True)

    class Meta:
        model = Deck
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
