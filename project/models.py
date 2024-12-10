from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    join_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique join link token

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('member', 'Member'), ('admin', 'Admin')])
    date_joined = models.DateTimeField(auto_now_add=True)

class GroupExpense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    split_type = models.CharField(max_length=20, choices=[('equal', 'Equal'), ('custom', 'Custom')])

class Split(models.Model):
    expense = models.ForeignKey(GroupExpense, on_delete=models.CASCADE, related_name="splits")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')])

class Itinerary(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="itineraries")
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.CharField(max_length=100)

class ItineraryItem(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[('flight', 'Flight'), ('accommodation', 'Accommodation'), ('activity', 'Activity')])
    day = models.PositiveIntegerField(blank=True, null=True)  # New field for "Day"

    def __str__(self):
        return self.title


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # Description of the activity
    timestamp = models.DateTimeField(default=now)  # Time of the action
    related_group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"