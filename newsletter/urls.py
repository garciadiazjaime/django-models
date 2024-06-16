from django.urls import path

from newsletter.views import (
    SubscriberViewSet,
)


urlpatterns = [
    path("", SubscriberViewSet.as_view()),
]
