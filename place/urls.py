from django.urls import path

from .views import (
    PlaceViewSet,
)


urlpatterns = [
    path("", PlaceViewSet.as_view()),
    path("<int:pk>", PlaceViewSet.as_view()),
]
