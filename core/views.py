from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from accounts.models import Profile, Deck, PlayerCard, DeckCard
from core.forms import DeckForm
from core.models import Card

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            kwargs['number_cards'] = PlayerCard.objects.filter(profile=profile).count()

        return super().dispatch(request, *args, **kwargs)


class CardListView(ListView):
    model = Card
    context_object_name = 'card_list'
    template_name = 'core/card_list.html'
    queryset = Card.objects.all()
    paginate_by = 25

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CardDetailView(DetailView):
    model = Card

    @staticmethod
    def card_detail_view(request, primary_key):
        card = get_object_or_404(Card, pk=primary_key)

        return render(request, 'core/card_detail.html', context={'card': card})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeckListView(ListView):
    model = Deck
    context_object_name = 'deck_list'
    template_name = 'core/deck_list.html'
    paginate_by = 25

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        return Deck.objects.filter(profile=profile)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeckDetailView(DetailView):
    model = Deck
    template_name = "core/deck_detail.html"

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        return Deck.objects.filter(profile=profile)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['deck_cards'] = DeckCard.objects.filter(deck=kwargs['object'])

        return super().get_context_data(**kwargs)


class DeckCreateView(CreateView):
    template_name = 'core/deck_edit.html'
    success_url = reverse_lazy('deck_list')
    form_class = DeckForm
    context_object_name = 'deck'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        profile = Profile.objects.filter(user=self.request.user).first()

        player_card_list = PlayerCard.objects.filter(profile=profile)

        kwargs.update({'player_card_list': player_card_list, 'deck_cards': None})

        return super().get_context_data(**kwargs)

    def _create_deck(self, form, request):
        profile = Profile.objects.filter(user=self.request.user).first()

        deck = form.save(commit=False)
        deck.profile = Profile.objects.filter(user=self.request.user).first()
        deck.save()

        player_cards_ids = request.POST.getlist('cards')

        for player_card_id in player_cards_ids:
            player_card = PlayerCard.objects.filter(id=player_card_id, profile=profile).first()

            deck_card = DeckCard.objects.filter(player_card=player_card, deck=deck).first()
            if not deck_card:
                deck_card = DeckCard(player_card=player_card, deck=deck)

            deck_card.save()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self._create_deck(form, request)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# noinspection PyAttributeOutsideInit
class DeckUpdateView(UpdateView):
    template_name = 'core/deck_edit.html'
    success_url = reverse_lazy('deck_list')
    context_object_name = 'deck'
    form_class = DeckForm

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        return Deck.objects.filter(profile=profile)

    def get_context_data(self, **kwargs):
        profile = Profile.objects.filter(user=self.request.user).first()

        player_card_list = PlayerCard.objects.filter(profile=profile)
        deck_cards = DeckCard.objects.filter(deck=self.object)

        kwargs.update({'player_card_list': player_card_list, 'deck_cards': deck_cards})

        return super().get_context_data(**kwargs)

    def _update_deck(self, form, request):
        profile = Profile.objects.filter(user=self.request.user).first()

        self.object = form.save()

        player_cards_ids = request.POST.getlist('cards')

        for player_card_id in player_cards_ids:
            player_card = PlayerCard.objects.filter(id=player_card_id, profile=profile).first()

            deck_card = DeckCard.objects.filter(player_card=player_card, deck=self.object).first()

            if not deck_card:
                deck_card = DeckCard(player_card=player_card, deck=self.object)

            deck_card.save()

        deck_cards = DeckCard.objects.filter(deck=self.object)
        for deck_card in deck_cards:
            player_card_id = deck_card.player_card.id
            if str(player_card_id) not in player_cards_ids:
                deck_card.delete()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            self._update_deck(form, request)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeckDelete(DeleteView):
    model = Deck
    success_url = reverse_lazy('deck_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ShopView(TemplateView):
    template_name = 'core/shop.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            # TODO fix the following line
            # kwargs['number_cards'] = PlayerCard.objects.filter(profile=profile).aggregate(Sum("numbercards"))
        return super().dispatch(request, *args, **kwargs)


class Pay2WinView(TemplateView):
    template_name = 'core/realmoneyshop.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            # TODO fix the following line
            # kwargs['number_cards'] = PlayerCard.objects.filter(profile=profile).aggregate(Sum("numbercards"))
        return super().dispatch(request, *args, **kwargs)
