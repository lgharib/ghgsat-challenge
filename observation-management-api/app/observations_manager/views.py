from django.contrib.auth.models import User, Group
from observations_manager.serializers import TargetSerializer, ObservationSerializer
from observations_manager.models import Target, Observation
from rest_framework import viewsets, renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics
from rest_framework.decorators import api_view, renderer_classes
from django.utils.dateparse import parse_date
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon


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

        start_timestamp = str(
            self.request.query_params.get('start_timestamp', None))
        end_timestamp = str(
            self.request.query_params.get('end_timestamp', None))

        if bounding_box is not None:
            queryset = queryset.filter(image_polygon__coveredby=bounding_box,
                                       timestamp__range=(start_timestamp, end_timestamp))
        return queryset


@api_view(['GET'])
@renderer_classes([renderers.StaticHTMLRenderer])
def search_target_kml(request, format=None):
    """
    A view that returns a kml file for targets given a bounding box
    """
    queryset = Target.objects.all()

    bounding_box = request.query_params['bounding_box']

    if bounding_box == '':
        bounding_box = None

    if bounding_box is not None:
        queryset = queryset.filter(coordinates__coveredby=bounding_box)

    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns, 'docid', 'GHGSat Document', 'Display GHGSat targets')
    k.append(d)
    f = kml.Folder(ns, 'folder1', 'Targets', 'Targets features')
    d.append(f)

    for target in queryset:
        p = kml.Placemark(ns, str(target.id), str(target.name), 'description')
        p.geometry = Point(target.coordinates.x,
                           target.coordinates.y, target.elevation)
        f.append(p)

    return Response(k.to_string(prettyprint=True))


@api_view(['GET'])
@renderer_classes([renderers.StaticHTMLRenderer])
def search_observations_kml(request, format=None):
    """
    A view that returns a kml file for observations given a bounding box and time period
    """
    queryset = Observation.objects.all()

    bounding_box = request.query_params['bounding_box']
    start_timestamp = request.query_params['start_timestamp']
    end_timestamp = request.query_params['end_timestamp']

    if bounding_box == '':
        bounding_box = None

    if bounding_box is not None:
        queryset = queryset.filter(image_polygon__coveredby=bounding_box,
                                   timestamp__range=(
                                       start_timestamp, end_timestamp))

    output = """
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document id="docid">
        <name>GHGSat Document</name>
        <description>Display GHGSat overlays</description>
        <visibility>1</visibility>
        <Folder id="folder1">
            <name>Ground Overlays</name>
            <description>Bouding box Ground overlays</description>
            <visibility>1</visibility>
    """

    for observation in queryset:
        output = output + """
            <GroundOverlay>
                <name>""" + str(observation.target.name) + """</name>
                <visibility>1</visibility>
                <description>Overlay Description.</description>
                <Icon>
                    <href>""" + str(observation.image_url) + """</href>
                </Icon>
                <LatLonBox>
                    <north>""" + str(observation.image_polygon.extent[0]) + """</north>
                    <south>""" + str(observation.image_polygon.extent[2]) + """</south>
                    <east> """ + str(observation.image_polygon.extent[1]) + """</east>
                    <west> """ + str(observation.image_polygon.extent[3]) + """</west>
                </LatLonBox>
                <TimeStamp>
				  <when>""" + str(observation.timestamp) + """</when>
				</TimeStamp>
            </GroundOverlay>
            """

    output = output + """
        </Folder>
    </Document>
    </kml>
    """

    return Response(output)
