import random
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from accounts.models import Profile, Deck, ProfileSubscriptions, DeckCard, PlayerCard
from combat.services import get_auto_or_manual_decks, cards_query_set_to_session


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
        if not request.GET['profile_deck'] or not request.GET['target_deck']:
            return redirect('combat')

        profile_deck = Deck.objects.filter(id=request.GET['profile_deck']).first()
        target_deck = Deck.objects.filter(id=request.GET['target_deck']).first()

        kwargs['profile_deck_cards'] = DeckCard.objects.filter(deck=profile_deck)
        kwargs['target_deck_cards'] = DeckCard.objects.filter(deck=target_deck)
        kwargs['profile'] = profile_deck.profile
        kwargs['target'] = target_deck.profile

        cards_query_set_to_session(self.request, kwargs['profile_deck_cards'], 'profile_deck_cards')
        cards_query_set_to_session(self.request, kwargs['target_deck_cards'], 'target_deck_cards')

        return super().dispatch(request, *args, **kwargs)


def combat_action(request):
    if request.method != 'POST':
        raise Http404()

    profile_deck_cards = request.session.get('profile_deck_cards')
    target_deck_cards = request.session.get('target_deck_cards')

    selected_player_card_id = request.POST['player_card']
    selected_player_card = profile_deck_cards[selected_player_card_id]
    del profile_deck_cards[selected_player_card_id]

    selected_target_card_id, selected_target_card = random.choice(list(target_deck_cards.items()))
    del target_deck_cards[selected_target_card_id]

    winner = "target_%s" % (selected_target_card['player_card'])
    looser = "profile_%s" % (selected_player_card['player_card'])
    player_state = 'looser'

    if selected_player_card['card_attack'] >= selected_target_card['card_health']:
        winner = "profile_%s" % (selected_player_card['player_card'])
        looser = "target_%s" % (selected_target_card['player_card'])
        player_state = 'winner'

    return JsonResponse({
        'profile_player_card': profile_deck_cards,
        'selected_target_card': selected_target_card,
        'winner': winner,
        'looser': looser,
        'player_state': player_state
    })
