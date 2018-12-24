from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView, CreateView, DeleteView, ListView

from accounts import services
from accounts.forms import ProfileSubscribeForm
from accounts.models import Profile, ProfileSubscriptions, ProfileAction, PlayerCard, Message, DeckCard
from core import constant
from core.services import log_profile_activity

from django.db.models import Q


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
        kwargs['profile'] = profile

        return super().dispatch(request, *args, **kwargs)


class ProfileSubscriptionDeleteView(DeleteView):
    model = ProfileSubscriptions
    success_url = reverse_lazy('dashboard')
    template_name = "account/profile_subscription/confirm_delete.html"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        profile = Profile.objects.filter(user=self.request.user).first()
        log_profile_activity(profile, constant.PROFILE_UNSUBSCRIBE)

        obj = super().get_object()
        if not obj.profile == profile:
            raise Http404

        return obj


class ProfileCardListView(ListView):
    model = PlayerCard
    context_object_name = 'player_card_list'
    template_name = 'account/player_card_list.html'
    paginate_by = 25

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        return PlayerCard.objects.filter(profile=profile)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProfileUserCardListView(ListView):
    model = PlayerCard
    context_object_name = 'player_card_list'
    template_name = 'account/player_card_list.html'
    paginate_by = 25
    pk = -1

    def get_queryset(self, *args, **kwargs):
        profile = Profile.objects.filter(id=self.pk).first()

        return PlayerCard.objects.filter(profile=profile)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']

        return super().dispatch(request, *args, **kwargs)


class MessageView(TemplateView):
    template_name = "account/messages.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=self.request.user).first()
        followers = ProfileSubscriptions.objects.filter(subscription=profile)
        subscriptions = ProfileSubscriptions.objects.filter(profile=profile)
        profiles = []
        for follower in followers:
            profiles.append(follower.profile)
        for subscription in subscriptions:
            profiles.append(subscription.subscription)

        contact = Profile.objects.filter(user=kwargs['pk']).first()

        kwargs['contact'] = contact
        kwargs['profiles'] = profiles
        kwargs['conversations'] = services.fetch_conversations(profile, contact)

        return super().dispatch(request, *args, **kwargs)


def post_chat_message(request):
    if request.method != 'POST':
        raise Http404()

    profile = Profile.objects.filter(user=request.user).first()
    contact = Profile.objects.filter(id=request.POST['contact']).first()

    Message.objects.create(profile=profile, receiver=contact, content=request.POST['message'])

    return JsonResponse({})


def get_chat_messages(request):
    if request.method != 'GET':
        raise Http404()

    profile = Profile.objects.filter(user=request.user).first()
    contact = request.GET['contact']

    return JsonResponse({
        'conversations': services.fetch_conversations(profile, contact)
    })


class TradeCardCenterView(TemplateView):
    template_name = "account/trade.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        identifier = kwargs['pk']
        profile = Profile.objects.filter(user=self.request.user).first()

        contact_profile_subscription = ProfileSubscriptions.objects.filter(id=identifier).first()
        contact = contact_profile_subscription.subscription

        kwargs['profile'] = profile
        kwargs['contact'] = contact
        kwargs['profile_cards'] = PlayerCard.objects.filter(profile=profile)
        kwargs['contact_cards'] = PlayerCard.objects.filter(profile=contact)

        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        contact = kwargs['contact']
        profile_card_id = request.POST['profile_player_card']
        profile_card = PlayerCard.objects.filter(id=profile_card_id).first()
        profile_card.profile = contact
        profile_card.save()

        profile = kwargs['profile']
        contact_card_id = request.POST['contact_player_card']
        contact_card = PlayerCard.objects.filter(id=contact_card_id).first()
        contact_card.profile = profile
        contact_card.save()

        messages.info(request, 'Successfully traded %s %s to %s %s' % (
            profile,
            profile_card.card.name,
            contact,
            contact_card.card.name
        ))

        return redirect('profile_user_card_trade', kwargs['pk'])
