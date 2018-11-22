from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/subscription/add', views.ProfileSubscriptionCreateView.as_view(), name='subscription_add'),
    path('dashboard/subscription/<int:pk>', views.ProfileSubscriptionDetailView.as_view(), name='subscription_detail'),
]
