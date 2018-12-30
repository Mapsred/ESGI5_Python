from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from accounts.models import Profile, Deck, PlayerCard, DeckCard
from core import constant
from core.forms import DeckForm
from core.models import Card

import logging

# Get an instance of a logger
from core.services import log_profile_activity

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

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        selling = request.POST['price']
        selling = int(selling)
        if selling == 1:
            profile = kwargs['profile']
            profile.credits = profile.credits + selling
            profile.save()
            messages.warning(request, 'You get 1 credit for this card')
            return redirect('home')
        else:
            messages.warning(request, 'You doesnt have this card')
            return redirect('shop')


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['deck_cards'] = DeckCard.objects.filter(deck=kwargs['object'])
        profile = Profile.objects.filter(user=self.request.user).first()
        kwargs['is_current_user'] = profile == kwargs['object'].profile
        kwargs['profile'] = profile

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
            profile = Profile.objects.filter(user=self.request.user).first()
            log_profile_activity(profile, constant.DECK_CREATE)

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
            profile = Profile.objects.filter(user=self.request.user).first()
            log_profile_activity(profile, constant.DECK_UPDATE)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeckDeleteView(DeleteView):
    model = Deck
    success_url = reverse_lazy('deck_list')
    template_name = "core/deck_confirm_delete.html"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        profile = Profile.objects.filter(user=self.request.user).first()
        log_profile_activity(profile, constant.DECK_DELETE)
        obj = super().get_object()
        if not obj.profile == profile:
            raise Http404

        return obj


class ShopView(TemplateView):
    template_name = 'core/shop.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
        return super().dispatch(request, *args, **kwargs)


class Pay2WinView(TemplateView):
    template_name = 'core/realmoneyshop.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            kwargs['profile'] = profile
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        credit = request.POST['credit']
        credit = int(credit)
        profile = kwargs['profile']

        if profile.credits < credit:
            profile.credits = profile.credits + credit
            profile.save()
            messages.warning(request, 'Congratulation!')

            return redirect('realmoneyshop')
        else:
            messages.warning(request, 'You have already too much gold')

            return redirect('realmoneyshop')


class NewDeckCard(TemplateView):
    template_name = 'core/new_deck_card.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            kwargs['profile'] = profile

            if "cards" in request.GET:
                cards = request.GET['cards'].split(",")
                playercards = []

                for card in cards:
                    card = PlayerCard.objects.filter(id=card).first()
                    playercards.append(card)

                kwargs['playercards'] = playercards

        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        price = request.POST['price']
        price = int(price)
        profile = kwargs['profile']

        if profile.credits >= price:
            profile.credits = profile.credits - price
            profile.save()

            if price == 100:
                cards = Card.objects.all().order_by('?')[:6]
            else:
                cards = Card.objects.all().order_by('?')[:30]

            url_parameter = []
            for card in cards:
                player_cards = PlayerCard(profile=profile, card=card)
                player_cards.save()
                url_parameter.append(player_cards.id)

            messages.success(request, 'You get new cards')

            url = resolve_url('new_deck_card')
            full_url = "%s?%s" % (url, urlencode({
                "cards": ','.join(map(str, url_parameter))
            }))

            return HttpResponseRedirect(full_url)
        else:
            messages.warning(request, 'Not enought credit, you have %s and you need %s' % (profile.credits, price))

            return redirect('shop')


class CardSelling(TemplateView):
    model = Card

    @staticmethod
    def card_detail_view(request, primary_key):
        card = get_object_or_404(Card, pk=primary_key)

        return render(request, 'core/card_detail.html', context={'card': card})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            kwargs['profile'] = profile

        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        selling = request.POST['selling']
        selling = int(selling)
        profile = kwargs['profile']

        if PlayerCard.objects.filter(profile=profile, card=selling).count() > 0:

            playercard = PlayerCard.objects.filter(profile=profile, card=selling).first()
            playercard.delete()

            profile.credits = profile.credits + 1
            profile.save()
            messages.warning(request, 'You get 1 credit for this card')

            return redirect('home')
        else:
            messages.warning(request, 'You dont have this card')

            return redirect('shop')
