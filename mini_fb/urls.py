from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import ShowAllProfilesView  # Corrected view import
from .views import ShowProfilePageView 
from .views import CreateProfileView
from .views import CreateStatusMessageView
from .views import UpdateProfileView
from.views import DeleteStatusMessageView
from .views import UpdateStatusMessageView
from .views import CreateFriendView
from .views import ShowFriendSuggestionsView
from .views import ShowNewsFeedView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    
    # Keep `pk` in `show_profile` for individual profile view
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),

    # Update paths to remove `pk` for these specific views as instructed
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('status/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="create_friend"),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name='news_feed'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]