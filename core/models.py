from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


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

    def image(self):
        return self.img_gold if self.img_gold is not None else self.img

    def image_type(self):
        return "img_gold" if self.img_gold is not None else "img"

    def __str__(self):
        return "[%s] - %s" % (self.card_id, self.name)
