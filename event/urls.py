from django.urls import path

from .views import (
    EventViewSet,
    LocationViewSet,
    MetadataViewSet,
    ArtistViewSet,
    ArtistMetadataViewSet,
    SpotifyViewSet,
)


urlpatterns = [
    path("", EventViewSet.as_view()),
    path("<int:pk>/", EventViewSet.as_view()),
    path("locations/", LocationViewSet.as_view()),
    path("metadata/", MetadataViewSet.as_view()),
    path("artists/", ArtistViewSet.as_view()),
    path("artists/metadata", ArtistMetadataViewSet.as_view()),
    path("spotify/<int:pk>/", SpotifyViewSet.as_view()),
]
