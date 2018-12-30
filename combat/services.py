from django.forms import model_to_dict

from accounts.models import Deck


def get_auto_or_manual_decks(parameters, profile, parameter_key):
    if parameters[parameter_key] == '_auto':
        return Deck.objects.filter(profile=profile).order_by('?')[:1].first().id
    else:
        return parameters[parameter_key]


def cards_query_set_to_session(request, queryset, key):
    profile_deck_cards = {}
    for profile_deck_card in queryset:
        player_card = profile_deck_card.player_card
        profile_deck_cards[player_card.id] = model_to_dict(profile_deck_card)
        profile_deck_cards[player_card.id]['card_name'] = player_card.card.name
        profile_deck_cards[player_card.id]['card_health'] = player_card.card.health
        profile_deck_cards[player_card.id]['card_attack'] = player_card.card.attack

    request.session[key] = profile_deck_cards
