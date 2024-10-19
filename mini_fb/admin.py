from django.contrib import admin
from .models import Profile
from .models import StatusMessage
from .models import Image

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city')


@admin.register(StatusMessage)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'message', 'profile')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_file', 'status_message', 'timestamp')