from django.urls import path
from .views import home_view, recent_tracks_view, test_env_view

app_name = 'rb'

urlpatterns = [
    path("", home_view, name="home"),
    path("recent-tracks/", recent_tracks_view, name="recent-tracks"),
    path("test-env/", test_env_view, name="test-env"),
] 