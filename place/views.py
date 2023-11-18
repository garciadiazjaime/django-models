from rest_framework import generics
from rest_framework import mixins
from rest_framework import filters
from django_filters import rest_framework as django_filters


from .models import Place
from .serializer import PlaceSerializer
from .filters import PlaceFilter


class PlaceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Place.objects.filter(permanently_closed=False)
    serializer_class = PlaceSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]
    filterset_class = PlaceFilter
    search_fields = ["types"]
    ordering_fields = ["user_ratings_total"]
    ordering = ["-user_ratings_total"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
