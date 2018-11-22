from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView, CreateView

from accounts.forms import ProfileSubscribeForm
from accounts.models import Profile, ProfileSubscriptions
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
    success_url = reverse_lazy('deck_list')
    form_class = ProfileSubscribeForm
    context_object_name = 'object'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["choices"] = Profile.objects.all()

        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            profile = Profile.objects.filter(user=self.request.user).first()
            log_profile_activity(profile, constant.PROFILE_SUBSCRIBE)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
