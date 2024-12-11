from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now

class Group(models.Model):
    """
    Represents a group for organizing expenses and itineraries.
    Fields:
    - name: The name of the group.
    - description: A brief description of the group.
    - created_at: The date and time the group was created.
    - join_token: A unique token generated using UUID to create a sharable join link for the group.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #Uses uuid for generating the join token url 
    join_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  

class Membership(models.Model):
    """
    Represents a user's membership in a group.
    
    Fields:
    - user: The user who is a member of the group.
    - group: The group the user belongs to.
    - role: The user's role in the group, either 'member' or 'admin'.
    - date_joined: The date and time the user joined the group.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('member', 'Member'), ('admin', 'Admin')])
    date_joined = models.DateTimeField(auto_now_add=True)

class GroupExpense(models.Model):
    """
    Represents an expense shared within a group.
    
    Fields:
    - group: The group associated with this expense.
    - payer: The user who paid for the expense.
    - amount: The total amount of the expense.
    - description: A brief description of the expense.
    - date: The date of the expense.
    - split_type: The method used to split the expense ('equal' or 'custom').
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    split_type = models.CharField(max_length=20, choices=[('equal', 'Equal'), ('custom', 'Custom')])

class Split(models.Model):
    """
    Represents a user's share of an expense in a group.
    
    Fields:
    - expense: The group expense associated with this split.
    - user: The user who owes or is owed a part of the expense.
    - amount: The amount the user owes or is owed.
    - status: The payment status for this split ('unpaid' or 'paid').
    """
    expense = models.ForeignKey(GroupExpense, on_delete=models.CASCADE, related_name="splits")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')])

class Itinerary(models.Model):
    """
    Represents a travel itinerary for a group.
    
    Fields:
    - group: The group associated with this itinerary.
    - start_date: The start date of the itinerary.
    - end_date: The end date of the itinerary.
    - destination: The destination of the trip.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="itineraries")
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.CharField(max_length=100)

class ItineraryItem(models.Model):
    """
    Represents a specific item in an itinerary, such as a flight or activity.
    
    Fields:
    - itinerary: The itinerary this item belongs to.
    - title: The title of the itinerary item.
    - description: Additional details about the item (optional).
    - date_time: The date and time of the itinerary item.
    - location: The location where the item occurs.
    - category: The type of the itinerary item (e.g., 'flight', 'accommodation', 'activity').
    - day: The day number in the itinerary (optional).
    """
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
    """
    Tracks user activity within the application.
    
    Fields:
    - user: The user who performed the action.
    - action: A description of the activity performed.
    - timestamp: The date and time the activity occurred (defaults to now).
    - related_group: The group associated with the activity (optional).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # Description of the activity
    timestamp = models.DateTimeField(default=now)  # Time of the action
    related_group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"