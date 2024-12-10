# project/urls.py
from django.urls import path
from .views import GroupListView, GroupDetailView, DashboardView, UserGroupsView, CreateGroupView, AddItineraryItemView, AddExpenseView, JoinGroupViaTokenView, GroupExpensesView, UpdateItineraryItemView, DeleteItineraryItemView, UpdateExpenseView, DeleteExpenseView
from . import views  
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  # Dashboard
    path('groups/', UserGroupsView.as_view(), name='user_groups'),  # User Groups
    path('groups/create/', CreateGroupView.as_view(), name='create_group'),  # Create Group
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),  # Group Detail
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), #Login View 
    path('groups/<int:group_id>/add_itinerary_item/', AddItineraryItemView.as_view(), name='add_itinerary_item'),
    path('groups/<int:group_id>/add_expense/', AddExpenseView.as_view(), name='add_expense'),
    path('groups/invite/<uuid:join_token>/', JoinGroupViaTokenView.as_view(), name='join_group_via_token'),
    path('groups/<int:pk>/expenses/', GroupExpensesView.as_view(), name='group_expenses'),
    path('itinerary-item/<int:pk>/update/', UpdateItineraryItemView.as_view(), name='update_itinerary_item'),
    path('itinerary-item/<int:pk>/delete/', DeleteItineraryItemView.as_view(), name='delete_itinerary_item'),
    path('expenses/<int:pk>/update/', UpdateExpenseView.as_view(), name='update_expense'),
    path('expenses/<int:pk>/delete/', DeleteExpenseView.as_view(), name='delete_expense'),


]