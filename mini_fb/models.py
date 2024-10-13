from django.db import models
from django.urls import reverse


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_pic = models.CharField(max_length=255, blank=True, null=True) 

    def get_status_messages(self):
        # Use the 'related_name' from the StatusMessage model (status_messages)
        return self.status_messages.all().order_by('-timestamp')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=280)  # Add max_length
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.profile.first_name}'s Message: {self.message[:50]}"  # Show first 50 characters of the message
    
    
