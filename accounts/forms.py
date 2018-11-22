from django import forms

from accounts.models import ProfileSubscriptions


class ProfileSubscribeForm(forms.ModelForm):
    subscription = forms.ChoiceField(required=True)

    class Meta:
        model = ProfileSubscriptions
        fields = ['subscription']

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(ProfileSubscribeForm, self).__init__(*args, **kwargs)
        self.fields['subscription'].choices = choices
