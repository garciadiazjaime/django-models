from django.urls import path

from .views import (
    EventViewSet,
    LocationViewSet,
    MetadataViewSet,
    ArtistViewSet,
    EventRankViewSet,
)


urlpatterns = [
    path("", EventViewSet.as_view()),
    path("<int:pk>/", EventViewSet.as_view()),
    path("locations/", LocationViewSet.as_view()),
    path("metadata/", MetadataViewSet.as_view()),
    path("artists/", ArtistViewSet.as_view()),
    path("rank/", EventRankViewSet.as_view()),
]
