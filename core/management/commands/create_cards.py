import json

import requests
from django.core.management.base import BaseCommand, CommandError
from core.models import Card, CardType, CardSet


# noinspection PyMethodMayBeStatic
class Command(BaseCommand):
    help = 'Generate and add all cards'
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/types/Minion"
    key = "qeUo5GZ8BImshrvOry8whvSBI1Hyp1IorHOjsnWRjJawFgjI8h"

    def handle(self, *args, **options):
        self.clean_cards()
        cards = self.get_cards()
        card_type = self.get_card_type("Minion")

        for card_content in cards:
            card_keys = list(card_content.keys())
            if self.verify_card(card_keys) and not self.card_exists(card_content['cardId']):
                card = Card(
                    card_id=card_content['cardId'],
                    dbf_id=card_content['dbfId'],
                    name=card_content['name'],
                    card_set=self.get_card_set(card_content['cardSet']),
                    type=card_type,
                    text=card_content['text'],
                    health=card_content['health'],
                    attack=card_content['attack']
                )

                if "img" in card_keys:
                    card.img = card_content['img']

                if "imgGold" in card_keys:
                    card.img_gold = card_content['imgGold']

                card.save()

    def clean_cards(self):
        CardType.objects.all().delete()
        CardSet.objects.all().delete()
        Card.objects.all().delete()

    def verify_card(self, card_keys):
        mandatory_keys = ('cardId', 'dbfId', 'name', 'cardSet', 'type', 'text', 'health', 'attack')

        for key in mandatory_keys:
            if key not in card_keys:
                return False

        return True

    def get_card_set(self, name):
        card_set = CardSet.objects.filter(name=name).first()
        if not card_set:
            card_set = CardSet(name=name)
            card_set.save()

        return card_set

    def get_card_type(self, name):
        card_type = CardType.objects.filter(name=name).first()
        if not card_type:
            card_type = CardType(name=name)
            card_type.save()

        return card_type

    def card_exists(self, card_id):
        return Card.objects.filter(card_id=card_id).exists()

    def get_cards(self):
        r = requests.get(url=self.url, headers={'X-Mashape-Key': self.key}, verify=False)

        return json.loads(r.text)
