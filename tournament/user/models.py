from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registrated_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'UserModel'


class TournamentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    player1 = models.CharField(max_length=30)
    player2 = models.CharField(max_length=30)
    player3 = models.CharField(max_length=30)
    player4 = models.CharField(max_length=30)
    player5 = models.CharField(max_length=30)
    player6 = models.CharField(max_length=30)
    player7 = models.CharField(max_length=30)
    player8 = models.CharField(max_length=30)
    stared_at = models.DateField(default=timezone.now)
    slug = models.SlugField(unique=True,)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(TournamentModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'TournamentModel'

    def __str__(self):
        return self.user.username


class Match(models.Model):
    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE)
    tour = TournamentModel()
    player_choice = (
        (1, tour.player1),
        (2, tour.player2),
        (3, tour.player3),
        (4, tour.player4),
        (5, tour.player5),
        (6, tour.player6),
        (7, tour.player7),
        (8, tour.player8),
    )
    ROUND_CHOICE = (
        (1, 'quarter'),
        (2, 'semifinal'),
        (3, 'final'),
    )
    player1 = models.PositiveSmallIntegerField(default=1, choices=player_choice)
    player2 = models.PositiveSmallIntegerField(default=2, choices=player_choice)
    score1 = models.PositiveSmallIntegerField(default=0)
    score2 = models.PositiveSmallIntegerField(default=0)
    round_ch = models.SmallIntegerField(default=1, choices=ROUND_CHOICE)
