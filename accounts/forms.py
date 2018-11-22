from django import forms
from django.forms import Select

from accounts.models import ProfileSubscriptions, Profile


class ProfileSubscribeForm(forms.ModelForm):
    subscription = forms.ModelChoiceField(
        queryset=Profile.objects.none(),
        empty_label=None,
        widget=Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ProfileSubscriptions
        fields = ['subscription']

    def __init__(self, *args, **kwargs):
        exclusions = kwargs.pop('exclusions')
        super(ProfileSubscribeForm, self).__init__(*args, **kwargs)
        self.fields['subscription'].queryset = Profile.objects.exclude(id__in=exclusions)
