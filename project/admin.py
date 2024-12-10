# your_app/admin.py
from django.contrib import admin
from .models import Group, Membership, Itinerary, ItineraryItem, ActivityLog

# Register the Group and Membership models
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'date_joined')

# Register the Itinerary model
@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('destination', 'start_date', 'end_date', 'group')  # Display key fields in the list view
    list_filter = ('start_date', 'end_date')  # Add filters for dates
    search_fields = ('destination',)  # Add a search bar for the destination

# Register the ItineraryItem model
@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'itinerary', 'date_time', 'category', 'location')  # Key fields for the list view
    list_filter = ('category', 'date_time')  # Filter by category and date
    search_fields = ('title', 'location')  # Add a search bar for title and location

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'related_group')  # Fields to display in the admin list view
    list_filter = ('timestamp', 'related_group')  # Filters for the admin interface
    search_fields = ('action', 'user__username')  # Enable search by action description or username