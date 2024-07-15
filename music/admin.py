from django.contrib import admin
from .models import Song, Singer, Comment

admin.site.register(Song)
admin.site.register(Singer)
admin.site.register(Comment)
