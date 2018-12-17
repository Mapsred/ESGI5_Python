from django.db.models import Q

from accounts.models import Message, Deck


def get_auto_or_manual_decks(parameters, profile, parameter_key):
    if parameters[parameter_key] == '_auto':
        return Deck.objects.filter(profile=profile).order_by('?')[:1].first().id
    else:
        return parameters[parameter_key]
