from django.test import TestCase
from observations_manager.models import Target


class TestTargetCase(TestCase):
    def setUp(self):
        Target.objects.create(
            name="Target 1", coordinates="POINT(-15.232322 36.5656)", elevation=500)

    def test_target_was_created(self):
        target = Target.objects.get(name="Target 1")
        self.assertEqual(target.elevation, 500, msg=None)
