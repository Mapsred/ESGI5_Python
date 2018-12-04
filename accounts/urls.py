from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/subscription/add', views.ProfileSubscriptionCreateView.as_view(), name='subscription_add'),
    path('dashboard/subscription/<int:pk>', views.ProfileSubscriptionDetailView.as_view(), name='subscription_detail'),
    path('dashboard/subscription/<int:pk>/delete', views.ProfileSubscriptionDeleteView.as_view(), name='subscription_delete'),
    path('cards/list', views.ProfileCardListView.as_view(), name='profile_card_list'),
    path('cards/list/<int:pk>', views.ProfileUserCardListView.as_view(), name='profile_user_card_list'),
]
