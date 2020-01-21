from django.contrib.auth.models import User, Group
from observations_manager.serializers import TargetSerializer, ObservationSerializer
from observations_manager.models import Target, Observation
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics

class TargetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows target to be viewed or edited.
    """
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

class ObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows target to be viewed or edited.
    """
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

class TargetViewList(generics.ListAPIView):
    serializer_class = TargetSerializer

    def get_queryset(self):
        """
        This view should return a list of all the targets
        by filtering against a `bounding_box` query parameter.
        """
        queryset = Target.objects.all()
        bounding_box = self.request.query_params.get('bounding_box', None)
        if bounding_box is not None:
            queryset = queryset.filter(coordinates__coveredby=bounding_box)
        return queryset