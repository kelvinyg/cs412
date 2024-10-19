from django.urls import path
from .views import ShowAllView # our view class definition 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)