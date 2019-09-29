from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.register, name='register'),
    path('add_tournament/', views.add_tournament, name='add_tournament'),
    path('tournament/<slug:tournament_name_slug>/', views.show_tournament, name='show_tournament'),
    path('tournament/<slug:tournament_name_slug>/add_match/', views.add_match, name='add_match'),
    path('tournament/<slug:tournament_name_slug>/change/', views.change_tour, name='change_tour'),
    path('my_tournaments/', views.my_tours, name='my_tours'),
    path('tournament/<slug:tournament_name_slug>/<slug:match_id_slug>/', views.change_match, name='change_match'),

    path('home/', views.home, name='home'),
]
