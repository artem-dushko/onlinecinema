from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'exp_date')  # add 'exp_date' here

admin.site.register(Profile, ProfileAdmin)
