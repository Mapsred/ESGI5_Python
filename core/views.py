from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from accounts.models import Profile
from core.models import Card, Deck


class CardListView(ListView):
    model = Card
    context_object_name = 'card_list'
    template_name = 'core/card_list.html'
    queryset = Card.objects.all()
    paginate_by = 25


class CardDetailView(DetailView):
    model = Card

    @staticmethod
    def card_detail_view(request, primary_key):
        card = get_object_or_404(Card, pk=primary_key)

        return render(request, 'core/card_detail.html', context={'card': card})


class DeckListView(ListView):
    model = Deck
    context_object_name = 'deck_list'
    template_name = 'core/deck_list.html'
    paginate_by = 25

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        return Deck.objects.filter(profile=profile)


class DeckDetailView(DetailView):
    model = Deck

    @staticmethod
    def deck_detail_view(request, primary_key):
        deck = get_object_or_404(Deck, pk=primary_key)

        return render(request, 'core/deck_detail.html', context={'deck': deck})
