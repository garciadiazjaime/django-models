"""
URL configuration for mint_models project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from event.urls import urlpatterns as event_routes
from place.urls import urlpatterns as place_routes
from newsletter.urls import urlpatterns as newsletter_routes
from mint_models import views

urlpatterns = [
    path("api/events/", include(event_routes)),
    path("api/places/", include(place_routes)),
    path("api/newsletter/", include(newsletter_routes)),
    path("gifts/", include("gift.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        ".well-known/acme-challenge/<str:code>",
        views.challenge,
    ),
]
