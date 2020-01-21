from django.contrib.auth.models import User, Group
from observations_manager.serializers import TargetSerializer, ObservationSerializer
from observations_manager.models import Target, Observation
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


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