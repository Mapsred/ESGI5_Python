from django.db import models


# Create your models here.

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

    def __str__(self):
        return "[%s] - %s" % (self.card_id, self.name)
