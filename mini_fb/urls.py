from django.urls import path, include
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
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name = 'show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete',DeleteStatusMessageView.as_view(), name = "delete_status" ),
    path('status/<int:pk>/update',UpdateStatusMessageView.as_view(), name = "update_status" ),
    path('profile/<int:pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name = "create_friend"),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('accounts/', include('django.contrib.auth.urls')),
]