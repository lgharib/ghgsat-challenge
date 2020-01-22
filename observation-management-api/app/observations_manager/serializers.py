from observations_manager.models import Target, Observation
from rest_framework import serializers


class ObservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Observation
        fields = ('id', 'image_url', 'timestamp', 'target')

class TargetSerializer(serializers.ModelSerializer):

    observations = ObservationSerializer(many=True, read_only=True)

    class Meta:
        model = Target
        fields = ('id', 'name', 'coordinates', 'elevation', 'observations')
