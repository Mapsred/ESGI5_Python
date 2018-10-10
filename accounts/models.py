from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Card


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=200)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.user.username


class Deck(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card)

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        cards = Card.objects.all().order_by('?')[:30]
        profile.cards.set(cards)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
