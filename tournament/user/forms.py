from django import forms
from .models import UserModel, Match, TournamentModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PictureUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['image']


class TournamentForm(forms.ModelForm):
    name = forms.CharField(label='Tournament Name')
    player1 = forms.CharField()
    player2 = forms.CharField()
    player3 = forms.CharField()
    player4 = forms.CharField()
    player5 = forms.CharField()
    player6 = forms.CharField()
    player7 = forms.CharField()
    player8 = forms.CharField()

    class Meta:
        model = TournamentModel
        exclude = ('user', 'stared_at', 'slug')


class MatchForms(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ('tournament', 'slug')


class MatchUpdateForm(forms.Form):
    score1 = forms.IntegerField()
    score2 = forms.IntegerField()
