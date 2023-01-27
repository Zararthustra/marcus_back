from django.contrib import admin
from .models import Critic, Vote, Watchlist, Masterpiece

admin.site.register(Critic)
admin.site.register(Vote)
admin.site.register(Watchlist)
admin.site.register(Masterpiece)