from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, PictureUpdateForm, TournamentForm, MatchForms
from .models import UserModel, TournamentModel, Match
from django.http import HttpResponseRedirect


def login(request):
    return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            us_mod = UserModel(user=user)
            us_mod.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
        return render(request, 'home/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PictureUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.usermodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PictureUpdateForm()

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'home/profile.html', context)


def add_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tour_model = TournamentModel()
            tour_model.user = request.user
            tour_model.name = form.cleaned_data['name']
            tour_model.player1 = form.cleaned_data['player1']
            tour_model.player2 = form.cleaned_data['player2']
            tour_model.player3 = form.cleaned_data['player3']
            tour_model.player4 = form.cleaned_data['player4']
            tour_model.player5 = form.cleaned_data['player5']
            tour_model.player6 = form.cleaned_data['player6']
            tour_model.player7 = form.cleaned_data['player7']
            tour_model.player8 = form.cleaned_data['player8']

            tour_model.save()
            return redirect('profile')
    else:
        form = TournamentForm()
    return render(request, 'match_and_tours/add_tournament.html', {'form': form})


def show_tournament(request, tournament_name_slug=None):
    tour = TournamentModel.objects.get(slug=tournament_name_slug)
    return render(request, 'match_and_tours/show_tournament.html', {'tour': tour})


def home(request):
    tour = TournamentModel.objects.all().values('name', 'slug')
    return render(request, 'home/home.html', {'tour': tour})


def my_tours(request):
    if request.user.is_authenticated:
        tour = TournamentModel.objects.filter(user=request.user).values('name', 'slug')
    else:
        return HttpResponseRedirect('You have not a tournament')
    return render(request, 'home/home.html', {'tour': tour})


def add(request):
    if request.method == 'POST':
        form = MatchForms(request.POST)
        tour = TournamentModel.objects.get(slug='la-liga')
        form.name = tour
        if form.is_valid():
            form.save()
        return redirect('home')
    form = MatchForms()
    return render(request, 'home/add.html', {'form': form})

