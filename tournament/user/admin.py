from django.contrib import admin
from .models import UserModel, TournamentModel, Match

admin.site.register(UserModel)
admin.site.register(TournamentModel)
admin.site.register(Match)
