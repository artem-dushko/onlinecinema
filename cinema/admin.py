from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration', 'date_added')

admin.site.register(Video, VideoAdmin)