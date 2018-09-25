from django import forms

from core.models import Deck


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'cards']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
