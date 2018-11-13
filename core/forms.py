from django import forms

from accounts.models import Deck


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
