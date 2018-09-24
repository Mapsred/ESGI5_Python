from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from accounts.models import Profile


class CardSet(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class CardType(models.Model):
    name = models.CharField(max_length=256)


class Card(models.Model):
    card_id = models.CharField(max_length=256)
    dbf_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    player_class = models.CharField(max_length=256)
    health = models.IntegerField(default=1)
    attack = models.IntegerField(default=1)
    img = models.CharField(max_length=256, default=None, blank=True, null=True)
    img_gold = models.CharField(max_length=256, default=None, blank=True, null=True)
    mechanics = models.CharField(max_length=256, default=None, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('card_detail', args=[str(self.id)])

    def __str__(self):
        return "[%s] - %s" % (self.card_id, self.name)


class Deck(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return "%s (%s)" % (self.name, self.cards.count())


@receiver(pre_save, sender=Deck)
def pre_save_deck(sender, instance, **kwargs):
    if 8 > instance.cards.count():
        raise AttributeError("A deck cannot have more than 8 cards !")
