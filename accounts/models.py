from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
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


class ProfileAction(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    action = models.CharField(max_length=256, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = ArrayField(models.CharField(max_length=256), blank=True, null=True)


class ProfileSubscriptions(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    subscription = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscription')
    created_at = models.DateTimeField(auto_now_add=True)


class Deck(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class PlayerCard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)


class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    player_card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        cards = Card.objects.all().order_by('?')[:30]
        for card in cards:
            player_cards = PlayerCard.objects.filter(profile=profile, card=card).first()
            if not player_cards:
                player_cards = PlayerCard(profile=profile, card=card)

            player_cards.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
