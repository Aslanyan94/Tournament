from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, PictureUpdateForm, TournamentForm, MatchForms, MatchUpdateForm
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
        tour_user = User.objects.get(username=request.user.username)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.user = tour_user
            tour.save()
            return redirect('home')
    else:
        form = TournamentForm()
    return render(request, 'match_and_tours/add_tournament.html', {'form': form})


def add_match(request, tournament_name_slug=None):
    if request.method == 'POST':
        form = MatchForms(request.POST)
        tour = TournamentModel.objects.get(slug=tournament_name_slug)
        if form.is_valid():
            match = form.save(commit=False)
            match.tournament = tour
            match.save()
            return redirect('home')
    else:
        tour = TournamentModel.objects.get(slug=tournament_name_slug)
        form = MatchForms()
    return render(request, 'match_and_tours/add_match.html', {'tour': tour, 'form': form})


def show_tournament(request, tournament_name_slug=None):
    tour = TournamentModel.objects.get(slug=tournament_name_slug)
    match = Match.objects.filter(tournament=tour)
    match1 = match.filter(round_ch=1)
    match2 = match.filter(round_ch=2)
    match3 = match.filter(round_ch=3)
    return render(request, 'match_and_tours/show_tournament.html', {
        'tour': tour,
        'match1': match1,
        'match2': match2,
        'match3': match3,
        })


def home(request):
    tour = TournamentModel.objects.all().values('name', 'slug')
    return render(request, 'home/home.html', {'tour': tour})


def my_tours(request):
    if request.user.is_authenticated:
        tour = TournamentModel.objects.filter(user=request.user).values('name', 'slug')
    else:
        return HttpResponseRedirect('You have not a tournament')
    return render(request, 'home/home.html', {'tour': tour})


def change_tour(request, tournament_name_slug=None):
    tour = TournamentModel.objects.get(slug=tournament_name_slug)
    form = TournamentForm(instance=tour)
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'match_and_tours/add_tournament.html', {'form': form})


def change_match(request, tournament_name_slug=None, match_id_slug=None):
    tour = TournamentModel.objects.get(slug=tournament_name_slug)
    match = Match.objects.get(tournament=tour, slug=match_id_slug)
    form = MatchUpdateForm()
    if request.method == 'POST':
        form = MatchUpdateForm(request.POST)
        if form.is_valid():
            match.score1 = form.cleaned_data['score1']
            match.score2 = form.cleaned_data['score2']
            match.save()
            return redirect('home')
    return render(request, 'match_and_tours/change_match.html', {'form': form, 'match': match},)

