from observations_manager.models import Target, Observation
from rest_framework import serializers


class TargetSerializer(serializers.ModelSerializer):

    observations = serializers.StringRelatedField(many=True)

    class Meta:
        model = Target
        fields = ('id', 'name', 'coordinates', 'elevation', 'observations')

class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ('id', 'image_url', 'timestamp', 'target')
