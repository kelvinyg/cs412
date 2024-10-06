from django.urls import path
from .views import ShowAllProfilesView  # Corrected view import

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
]