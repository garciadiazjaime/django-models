from django.urls import path

from .views import (
    EventViewSet,
    LocationViewSet,
    GMapsLocationViewSet,
)


urlpatterns = [
    path("events/", EventViewSet.as_view()),
    path("locations/", LocationViewSet.as_view()),
    path("locations/<int:pk>/", LocationViewSet.as_view()),
    path("locations/gmaps/", GMapsLocationViewSet.as_view()),
]
