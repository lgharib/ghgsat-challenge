from django.contrib.auth.models import User, Group
from observations_manager.serializers import TargetSerializer, ObservationSerializer
from observations_manager.models import Target, Observation
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from django.utils.dateparse import parse_date


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

class ObservationViewList(generics.ListAPIView):
    serializer_class = ObservationSerializer

    def get_queryset(self):
        """
        This view should return a list of all the targets
        by filtering against a `bounding_box`, `start_timestamp`, 
        `end_timestamp` query parameters.
        """

        queryset = Observation.objects.all()

        bounding_box = self.request.query_params.get('bounding_box', None)
        
        start_timestamp = str(self.request.query_params.get('start_timestamp', None))
        end_timestamp = str(self.request.query_params.get('end_timestamp', None))

        if bounding_box is not None:
            queryset = queryset.filter(target__coordinates__coveredby=bounding_box, 
            timestamp__range=(start_timestamp, end_timestamp))
        return queryset