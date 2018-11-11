from django import forms

from core.models import Deck


class DeckForm(forms.ModelForm):
    name = forms.CharField(max_length=120, required=True)

    class Meta:
        model = Deck
        fields = ['name', 'cards']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
