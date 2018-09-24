from django.contrib import admin

# Register your models here.
from .models import Card, CardSet, CardType, Deck

admin.site.register(Card)
admin.site.register(CardSet)
admin.site.register(CardType)
admin.site.register(Deck)
