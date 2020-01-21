from django.test import TestCase
from observations_manager.models import Target, Observation
from datetime import datetime
import json

class TestTargetCase(TestCase):
    def setUp(self):
        Target.objects.create(
            name="Target 2", coordinates="POINT(-15.232322 36.5656)", elevation=500)
        Target.objects.create(
            name="Montreal Downtown", coordinates="POINT(-73.647013 45.532695)", 
            elevation=10)
        Target.objects.create(
            name="Montreal East North", 
            coordinates="POINT(-73.52874799999999 45.628445)", 
            elevation=10)
        Target.objects.create(
            name="Casablanca", 
            coordinates="POINT(-7.612291 33.577592)", 
            elevation=0)

    def test_target_is_created(self):
        target = Target.objects.get(name="Target 2")
        self.assertEqual(target.elevation, 500, msg=None)
    
    def test_api_target_is_created(self):
        data = {
            "name":"Target 2",
            "coordinates": "POINT(-15.232322 36.5656)",
            "elevation": "500"
        }
        response = self.client.post("/targets/", data, format='json')
        self.assertEqual(json.loads(response.content)['elevation'], 500)

    def test_api_targets_search_matching_bounding_box(self):
        data = {"bounding_box": "POLYGON((-74.150848 45.265222, -73.355713 45.790509, -73.355713 45.265222, -74.150848 45.265222, -74.150848 45.265222))"}
        response = self.client.get("/search_targets/", data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 2)

class TestObservationCase(TestCase):
    def setUp(self):
        target1 = Target.objects.create(
            name="Target 3", 
            coordinates="POINT(-15.232322 36.5656)", 
            elevation=500)

        target2 = Target.objects.create(
            name="Montreal Downtown", 
            coordinates="POINT(-73.647013 45.532695)", 
            elevation=10)

        target3 = Target.objects.create(
            name="Casablanca", 
            coordinates="POINT(-7.612291 33.577592)",
            elevation=10)

        Observation.objects.create(
            image_url="http://image-server/observations/LAT20LONG10202001201.png", 
            timestamp=datetime(2007, 12, 6, 16, 29, 43, 79043), 
            target = target1)

        Observation.objects.create(
            image_url="http://image-server/observations/LAT20LONG10202001202.png", 
            timestamp=datetime(2019, 12, 1, 16, 29, 43, 79043), 
            target = target2)

        Observation.objects.create(
            image_url="http://image-server/observations/LAT20LONG10202001203.png", 
            timestamp=datetime(2019, 12, 5, 8, 0, 0, 79043), 
            target = target2)

        Observation.objects.create(
            image_url="http://image-server/observations/LAT20LONG10202001203.png", 
            timestamp=datetime(2019, 12, 10, 9, 0, 0, 79043), 
            target = target2)

        Observation.objects.create(
            image_url="http://image-server/observations/LAT20LONG10202001204.png", 
            timestamp=datetime(2019, 12, 5, 9, 0, 0, 79043), 
            target = target3)

    def test_observation_is_created(self):
        observation1 = Observation.objects.get(
            image_url="http://image-server/observations/LAT20LONG10202001201.png")
        self.assertEqual(observation1.timestamp.replace(tzinfo=None), 
        datetime(2007, 12, 6, 16, 29, 43, 79043), msg=None)

    def test_api_observation_is_created(self):
        data1 = {
            "name":"Target 2",
            "coordinates": "POINT(-15.232322 36.5656)",
            "elevation": "500"
        }
        response1 = self.client.post("/targets/", data1, format='json')

        data2 = {
            "image_url":"https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2019-10-08T00:00:00Z&BBOX=33.167724609375,-7.9200439453125,33.802734375,-7.213623046875&CRS=EPSG:4326&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor,Coastlines,Reference_Features,Reference_Labels&WRAP=day,x,x,x&FORMAT=image/jpeg&WIDTH=643&HEIGHT=578&ts=1579645310910",
            "timestamp": "2019-06-27 22:00:33",
            "target": str(json.loads(response1.content)['id'])
        }
        response2 = self.client.post("/observations/", data2, format='json')

        self.assertEqual(json.loads(response2.content)['timestamp'], 
        "2019-06-27T22:00:33Z")

    def test_api_observations_search_matching_bounding_box_and_time_period(self):
        data = {"bounding_box": "POLYGON((-74.150848 45.265222, -73.355713 45.790509, -73.355713 45.265222, -74.150848 45.265222, -74.150848 45.265222))",
                "start_timestamp": "2019-12-01 00:00:00",
                "end_timestamp": "2019-12-06 23:59:59",
            }
        response = self.client.get("/search_targets/", data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 2)
