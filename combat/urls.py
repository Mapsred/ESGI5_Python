from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.CombatView.as_view(), name='combat'),
    path('action', views.CombatActionView.as_view(), name='combat_action'),
]
