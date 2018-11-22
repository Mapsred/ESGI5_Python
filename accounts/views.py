from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView, CreateView, DetailView

from accounts.forms import ProfileSubscribeForm
from accounts.models import Profile, ProfileSubscriptions, ProfileAction
from core import constant
from core.services import log_profile_activity


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            kwargs['followers'] = ProfileSubscriptions.objects.filter(subscription=profile)
            kwargs['subscriptions'] = ProfileSubscriptions.objects.filter(profile=profile)

        return super().dispatch(request, *args, **kwargs)


class ProfileSubscriptionCreateView(CreateView):
    template_name = 'account/profile_subscription/create.html'
    success_url = reverse_lazy('dashboard')
    form_class = ProfileSubscribeForm
    context_object_name = 'object'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        profile = Profile.objects.filter(user=self.request.user).first()
        subcribed_user_list = ProfileSubscriptions.objects.filter(profile=profile)

        exclusions = set()
        exclusions.add(profile.id)

        for subscribed in subcribed_user_list:
            exclusions.add(subscribed.subscription_id)

        kwargs["exclusions"] = list(exclusions)

        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            profile = Profile.objects.filter(user=self.request.user).first()

            subcription = form.save(commit=False)
            subcription.profile = profile
            subcription.save()

            log_profile_activity(profile, constant.PROFILE_SUBSCRIBE)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProfileSubscriptionDetailView(TemplateView):
    template_name = "account/profile_subscription/detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        identifier = kwargs['pk']

        profile = Profile.objects.filter(user=request.user).first()
        subscription_profile = get_object_or_404(ProfileSubscriptions, id=identifier, profile=profile)
        kwargs['subscription_profile'] = subscription_profile
        kwargs['profile_actions'] = ProfileAction.objects.filter(profile=subscription_profile.subscription)

        return super().dispatch(request, *args, **kwargs)
