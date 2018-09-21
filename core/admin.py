from django.contrib import admin

# Register your models here.
from .models import Card, CardSet, CardType

admin.site.register(Card)
admin.site.register(CardSet)
admin.site.register(CardType)
