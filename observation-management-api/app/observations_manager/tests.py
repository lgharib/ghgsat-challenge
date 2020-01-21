from django.test import TestCase
from observations_manager.models import Target, Observation
from datetime import datetime

class TestTargetCase(TestCase):
    def setUp(self):
        Target.objects.create(
            name="Target 2", coordinates="POINT(-15.232322 36.5656)", elevation=500)

    def test_target_is_created(self):
        target = Target.objects.get(name="Target 2")
        self.assertEqual(target.elevation, 500, msg=None)

class TestObservationCase(TestCase):
    def setUp(self):
        target1 = Target.objects.create(name="Target 3", 
        coordinates="POINT(-15.232322 36.5656)", 
        elevation=500)
        Observation.objects.create(
            image_url="http://image-server/observations/LAT20LONG10202001201.png", 
            timestamp=datetime.datetime(2007, 12, 6, 16, 29, 43, 79043), 
            target = target1)

    def test_observation_is_created(self):
        observation1 = Observation.objects.get(
            image_url="http://image-server/observations/LAT20LONG10202001201.png")
        self.assertEqual(observation1.timestamp, 
        datetime.datetime(2007, 12, 6, 16, 29, 43, 79043), msg=None)