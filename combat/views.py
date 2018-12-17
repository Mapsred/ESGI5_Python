from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from accounts.models import Profile, Deck, ProfileSubscriptions
from combat.services import get_auto_or_manual_decks


class CombatView(TemplateView):
    template_name = "combat/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        identifier = kwargs['pk']

        profile = Profile.objects.filter(user=request.user).first()
        target = ProfileSubscriptions.objects.filter(id=identifier).first()
        kwargs['profile'] = profile
        kwargs['target'] = target.subscription
        kwargs['profile_decks'] = Deck.objects.filter(profile=profile).all()
        kwargs['target_decks'] = Deck.objects.filter(profile=target.subscription).all()

        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        parameters = request.POST
        print(parameters)

        profile = kwargs['profile']
        target = kwargs['target']

        profile_deck = get_auto_or_manual_decks(parameters, profile, 'profile_deck')
        target_deck = get_auto_or_manual_decks(parameters, target, 'target_deck')

        url = resolve_url('combat_action')

        full_url = "%s?%s" % (url, urlencode({
            "profile_deck": profile_deck,
            "target_deck": target_deck
        }))

        return HttpResponseRedirect(full_url)


class CombatActionView(TemplateView):
    template_name = "combat/action.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        profile_deck = Deck.objects.filter(id=request.GET['profile_deck']).first()
        target_deck = Deck.objects.filter(id=request.GET['target_deck']).first()

        kwargs['profile_deck'] = profile_deck
        kwargs['target_deck'] = target_deck
        kwargs['profile'] = profile_deck.profile
        kwargs['target'] = target_deck.profile

        return super().dispatch(request, *args, **kwargs)
