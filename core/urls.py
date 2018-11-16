from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cards/', views.CardListView.as_view(), name='card_list'),
    path('cards/<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
    path('decks/', views.DeckListView.as_view(), name='deck_list'),
    path('decks/<int:pk>', views.DeckDetailView.as_view(), name='deck_detail'),
    path('decks/add/', views.DeckCreateView.as_view(), name='deck_add'),
    path('decks/<int:pk>/edit', views.DeckUpdateView.as_view(), name='deck_edit'),
    path('decks/<int:pk>/delete', views.DeckDeleteView.as_view(), name='deck_delete'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('realmoneyshop/', views.Pay2WinView.as_view(), name='realmoneyshop'),
]
