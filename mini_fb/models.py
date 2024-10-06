from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_pic = models.CharField(max_length=255, blank=True, null=True)  # CharField for relative paths

    def __str__(self):
        return f"{self.first_name} {self.last_name}"