==========================
Observation Management API
==========================

This repository is hosting the API build for GHGSat challenge linked bellow

`Link to the challenge <https://github.com/GHGSat/tech-challenge/blob/master/webdev/README.md#challenge-3-observation-management>`_

.. image:: icons/map-24px.svg
    :width: 24px
    :align: left
    :height: 24px
    :alt: map

***************
API Description
***************


This GIS API let you:

#. Create Geospacial targets.
#. Create timestamped image observations associated to a specific target.
#. You can retrieve targets within a given coordinated bouding box.
#. You can retrieve observations within a given coordinated bounding box and within a specific period of time.

.. image:: icons/done-24px.svg
    :width: 24px
    :align: left
    :height: 24px
    :alt: info

************
Requirements
************

Download and install Docker and docker-compose

The following versions where used during the build of this project:

#. Docker version 19.03.5, build 633a0ea838
#. docker-compose version 1.17.1

.. image:: icons/info-24px.svg
    :width: 24px
    :align: left
    :height: 24px
    :alt: info

************
Installation
************

* cd observation-management-api
* docker-compose up -d --build
* Navigate to http://localhost:8000/

.. image:: icons/http-24px.svg
    :width: 24px
    :align: left
    :height: 24px
    :alt: info

*****
Usage
*****

Using a REST Client or Curl command you can use the API at the following endpoints with specific parameters

To create a new target
######################

Request
*******

/targets/

.. sourcecode:: json

        curl -X POST -H 'Content-Type: application/json' -i http://localhost:8000/targets/ --data '
        {
            "name": "Target 1",
            "coordinates": "POINT(-34.345345345 29.5654654)",
            "elevation": 500
        }'

Where coordinates is a standard GIS POINT with respectively Lng and Lat coordinates

Response
********

The response data is in json format:

.. sourcecode:: json

    {
        "id": 43,
        "name": "Target 1",
        "coordinates": "SRID=4326;POINT (-34.345345345 29.5654654)",
        "elevation": 500,
        "observations": []
    }

To create a new observation
###########################

Request
*******

/observations/

.. sourcecode:: json

    curl -X POST -H 'Content-Type: application/json' -i http://localhost:8000/observations/ --data '{
        "image_url": "https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2019-10-08T00:00:00Z&BBOX=33.167724609375,-7.9200439453125,33.802734375,-7.213623046875&CRS=EPSG:4326&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor,Coastlines,Reference_Features,Reference_Labels&WRAP=day,x,x,x&FORMAT=image/jpeg&WIDTH=643&HEIGHT=578&ts=1579645310910",
        "timestamp": "2019-06-27 22:00:33",
        "target": 43
    }'

Where timestamp has to respect the "YYYY-MM-DD HH:mm:ss" format

Response
********

The response data is in json format:

.. sourcecode:: json

    {
        "id": 44,
        "image_url": "https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2019-10-08T00:00:00Z&BBOX=33.167724609375,-7.9200439453125,33.802734375,-7.213623046875&CRS=EPSG:4326&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor,Coastlines,Reference_Features,Reference_Labels&WRAP=day,x,x,x&FORMAT=image/jpeg&WIDTH=643&HEIGHT=578&ts=1579645310910",
        "timestamp": "2019-06-27T22:00:33Z",
        "target": 43
    }

To search targets
#################

/search_targets/

Request
*******

.. sourcecode:: json

    curl -X GET -i 'http://localhost:8000/search_targets/?bounding_box=POLYGON((-74.150848 45.265222, -73.355713 45.790509, -73.355713 45.265222, -74.150848 45.265222, -74.150848 45.265222))'

Response
********

.. sourcecode:: json

    {
        "count": 4,
        "next": null,
        "previous": null,
        "results": [
            {
            "id": 41,
            "name": "Montreal East North",
            "coordinates": "SRID=4326;POINT (-73.52874799999999 45.628445)",
            "elevation": 10,
            "observations": []
            },
            {
            "id": 40,
            "name": "Montreal Downtown",
            "coordinates": "SRID=4326;POINT (-73.647013 45.532695)",
            "elevation": 10,
            "observations": []
            },
            {
            "id": 39,
            "name": "Montreal Nord Est",
            "coordinates": "SRID=4326;POINT (-73.52874799999999 45.628445)",
            "elevation": 10,
            "observations": []
            },
            {
            "id": 36,
            "name": "Montreal",
            "coordinates": "SRID=4326;POINT (-73.647013 45.532695)",
            "elevation": 10,
            "observations": [
                {
                "id": 45,
                "image_url": "https://emap-int.com/wp-content/uploads/2016/06/Honolulu-HI-USA-RE-740x470.jpg",
                "timestamp": "2019-12-09T00:00:00Z",
                "target": 36
                },
                {
                "id": 41,
                "image_url": "https://emap-int.com/wp-content/uploads/2016/06/Honolulu-HI-USA-RE-740x470.jpg",
                "timestamp": "2019-12-04T00:00:00Z",
                "target": 36
                }
            ]
            }
        ]
    }


To search observations
######################

/search_observations/

Request
*******

.. sourcecode:: json

    curl -X GET -i 'http://localhost:8000/search_observations/?start_timestamp=2019-12-01T00:00:00Z&end_timestamp=2019-12-10T23:59:59Z&bounding_box=POLYGON((-74.150848 45.265222, -73.355713 45.790509, -73.355713 45.265222, -74.150848 45.265222, -74.150848 45.265222))'

Response
********

.. sourcecode:: json

    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
            "id": 45,
            "image_url": "https://emap-int.com/wp-content/uploads/2016/06/Honolulu-HI-USA-RE-740x470.jpg",
            "timestamp": "2019-12-09T00:00:00Z",
            "target": 36
            },
            {
            "id": 41,
            "image_url": "https://emap-int.com/wp-content/uploads/2016/06/Honolulu-HI-USA-RE-740x470.jpg",
            "timestamp": "2019-12-04T00:00:00Z",
            "target": 36
            }
        ]
    }

*************
Execute Tests
*************

To execute tests execute the following commands:

* cd observation-management-api
* docker-compose -f docker-compose.yml exec web python manage.py test