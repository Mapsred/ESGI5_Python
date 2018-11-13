from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Card


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=200)

    def __str__(self):
        return self.user.username


class Deck(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class PlayerCard(models.Model):
    profilePlayer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cardPlayer = models.ForeignKey(Card, on_delete=models.CASCADE)
    numbercards = models.IntegerField(default=0)


class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    cardPlayer = models.ForeignKey(Card, on_delete=models.CASCADE)
    numbercards = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        cards = Card.objects.all().order_by('?')[:30]
        for card in cards:
            player_cards = PlayerCard.objects.filter(profilePlayer=profile, cardPlayer=card).first()
            if not player_cards:
                player_cards = PlayerCard(profilePlayer=profile, cardPlayer=card, numbercards=0)
            player_cards.numbercards += 1
            player_cards.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
