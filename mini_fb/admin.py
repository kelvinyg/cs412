from django.contrib import admin
from .models import Profile
from .models import StatusMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city')


@admin.register(StatusMessage)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'message', 'profile')