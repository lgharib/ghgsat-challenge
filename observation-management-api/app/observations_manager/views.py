from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from observations_manager.serializers import TargetSerializer
from observations_manager.models import Target


class TargetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows target to be viewed or edited.
    """
    queryset = Target.objects.all()
    serializer_class = TargetSerializer