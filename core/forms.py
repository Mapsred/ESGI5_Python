from django import forms

from accounts.models import Deck, Profile, PlayerCard


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeckForm, self).__init__(*args, **kwargs)
        profile = Profile.objects.filter(user=user).first()
        self.fields['cards'].queryset = PlayerCard.objects.filter(profile=profile)
