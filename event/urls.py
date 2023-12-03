from django.urls import path

from .views import (
    EventViewSet,
    LocationViewSet,
    GMapsLocationViewSet,
    ArtistViewSet,
    MetadataViewSet,
)


urlpatterns = [
    path("", EventViewSet.as_view()),
    path("artists/", ArtistViewSet.as_view()),
    path("artists/<int:pk>/", ArtistViewSet.as_view()),
    path("artists/metadata", MetadataViewSet.as_view()),
    path("locations/", LocationViewSet.as_view()),
    path("locations/<int:pk>/", LocationViewSet.as_view()),
    path("locations/gmaps/", GMapsLocationViewSet.as_view()),
    path("locations/metadata", MetadataViewSet.as_view()),
]
