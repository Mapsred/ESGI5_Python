from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Sum

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
            kwargs['number_cards'] = PlayerCard.objects.filter(profilePlayer=profile).aggregate(Sum("numbercards"))

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
        kwargs['cards'] = DeckCard.objects.filter(deck=kwargs['object'])

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

        card_list = PlayerCard.objects.filter(profilePlayer=profile)

        kwargs.update({'card_list': card_list, 'deck_cards': None})

        return super().get_context_data(**kwargs)

    def _create_deck(self, form, request):
        profile = Profile.objects.filter(user=self.request.user).first()

        deck = form.save(commit=False)
        deck.profile = Profile.objects.filter(user=self.request.user).first()
        deck.save()

        cards = request.POST.getlist('cards')
        for card in cards:
            player_card = PlayerCard.objects.filter(cardPlayer=card, profilePlayer=profile).first()
            card = player_card.cardPlayer

            deck_card = DeckCard.objects.filter(cardPlayer=card, deck=deck).first()
            if not deck_card:
                deck_card = DeckCard(cardPlayer=card, deck=deck, numbercards=0)

            deck_card.numbercards += 1
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

        card_list = PlayerCard.objects.filter(profilePlayer=profile)
        deck_cards = DeckCard.objects.filter(deck=self.object)

        kwargs.update({'card_list': card_list, 'deck_cards': deck_cards})

        return super().get_context_data(**kwargs)

    def _update_deck(self, form, request):
        profile = Profile.objects.filter(user=self.request.user).first()

        self.object = form.save()
        cards = request.POST.getlist('cards')
        deck_cards = DeckCard.objects.filter(deck=self.object)

        for deck_card in deck_cards:
            if str(deck_card.cardPlayer.id) not in cards:
                deck_card.delete()

        for card in cards:
            player_card = PlayerCard.objects.filter(cardPlayer=card, profilePlayer=profile).first()
            card = player_card.cardPlayer

            deck_card = DeckCard.objects.filter(cardPlayer=card, deck=self.object).first()
            if not deck_card:
                deck_card = DeckCard(cardPlayer=card, deck=self.object, numbercards=1)

            deck_card.save()

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
            kwargs['number_cards'] = PlayerCard.objects.filter(profilePlayer=profile).aggregate(Sum("numbercards"))
        return super().dispatch(request, *args, **kwargs)


class Pay2WinView(TemplateView):
    template_name = 'core/realmoneyshop.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            kwargs['number_cards'] = PlayerCard.objects.filter(profilePlayer=profile).aggregate(Sum("numbercards"))
        return super().dispatch(request, *args, **kwargs)