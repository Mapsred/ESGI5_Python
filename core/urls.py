from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.CardListView.as_view(), name='card_list'),
    path('<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
]
