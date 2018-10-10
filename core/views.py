from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from accounts.models import Profile, Deck
from core.forms import DeckForm
from core.models import Card

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile': Profile.objects.filter(user=self.request.user).first()
        })

        return context


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


class DeckCreateView(CreateView):
    template_name = 'core/deck_edit.html'
    success_url = reverse_lazy('deck_list')
    form_class = DeckForm
    context_object_name = 'deck'

    def get_form_kwargs(self):
        kwargs = super(DeckCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def form_valid(self, form):
        deck = form.save(commit=False)
        deck.profile = Profile.objects.filter(user=self.request.user).first()
        deck.save()
        form.save_m2m()

        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeckUpdateView(UpdateView):
    template_name = 'core/deck_edit.html'
    success_url = reverse_lazy('deck_list')
    context_object_name = 'deck'
    form_class = DeckForm

    def get_form_kwargs(self):
        kwargs = super(DeckUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        return Deck.objects.filter(profile=profile)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeckDelete(DeleteView):
    model = Deck
    success_url = reverse_lazy('deck_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
