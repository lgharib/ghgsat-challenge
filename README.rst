==========================
Observation Management API
==========================

This repository is hosting the API build for GHGSat challenge linked bellow

`Link to the challenge <https://github.com/GHGSat/tech-challenge/blob/master/webdev/README.md#challenge-3-observation-management>`_

***************
API Description
***************

This GIS API let you:

#. Create Geospacial targets.
#. Create timestamped image observations associated to a specific target.
#. You can retrieve targets within a given coordinated bouding box.
#. You can retrieve observations within a given coordinated bounding box and within a specific period of time.

************
Requirements
************

Download and install Docker and docker-compose

The following versions where used during the build of this project:

#. Docker version 19.03.5, build 633a0ea838
#. docker-compose version 1.17.1

************
Installation
************

* cd observation-management-api
* docker-compose up -d --build
* Navigate to http://localhost:8000/

*****
Usage
*****

Using a REST Client or Curl command you can use the API at the following endpoints with specific parameters

To create a new target
######################

Request
*******

/create_target

.. sourcecode:: json

        {
            "coordinates": {
                "lat": 10,
                "long": -20,
                "elevation": 500
            },
            "name": "Target 1"
        }

Response
********

The response data is a json with the target name and id

.. sourcecode:: json

        {
            "id": 1,
            "name": "Target 1"
        }

To create a new observation
###########################

Request
*******

/create_observation

.. sourcecode:: json

        {
            "image_url": "http://image-server/observations/LAT20LONG10202001201.png",
            "timestamp": 2020012,
            "target_id": 1
        }

Response
********

The response data is a json with the observation id

.. sourcecode:: json

        {
            "observation_id": 1
        }

To search targets
#################

Request
*******

The user can either request a json file with all targets or a KML file by specifying respectivly:

.. sourcecode:: json

        {
            "visualization": "json"
        }

or

.. sourcecode:: json

        {
            "visualization": "kml"
        }

/search_targets

.. sourcecode:: json

        {
            "elevation": 500,
            "visualization": "kml",
            "coordinates0": {
                "lat": 10,
                "long": -20
            },
            "coordinates1": {
                "lat": 11,
                "long": -20
            },
            "coordinates2": {
                "lat": 10,
                "long": -21
            },
            "coordinates3": {
                "lat": 11,
                "long": -21
            }
        }

Response
********

The response can either be a json file with the list of targets:

.. sourcecode:: json

        {
            0: {
                "id": 1,
                "name": "Target 1",
                "coordinates": {
                    "lat": 10,
                    "long": -20,
                    "elevation": 500
                }
            },
            1: {
                "id": 2,
                "name": "Target 2",
                "coordinates": {
                    "lat": 11,
                    "long": -22,
                    "elevation": 10
                }
            },
            2: {
                "id": 3,
                "name": "Target 3",
                "coordinates": {
                    "lat": 33,
                    "long": -55,
                    "elevation": 5
                }
            },
        }

Or a KML file

To search observations
######################

/search_observations

Request
*******

The user can either request a json file with all observations or a KML file by specifying respectivly:

.. sourcecode:: json

        {
            "visualization": "json"
        }

or

.. sourcecode:: json

        {
            "visualization": "kml"
        }

/search_targets

.. sourcecode:: json

        {
            "elevation": 500,
            "visualization": "kml",
            "start_timestamp": 20200101,
            "end_timestamp": 20200130,
            "coordinates0": {
                "lat": 10,
                "long": -20
            },
            "coordinates1": {
                "lat": 11,
                "long": -20
            },
            "coordinates2": {
                "lat": 10,
                "long": -21
            },
            "coordinates3": {
                "lat": 11,
                "long": -21
            }
        }

Response
********

The response can either be a json file with the list of targets:

.. sourcecode:: json

        {
            0: {
                "id": 0,
                "image_url": "http://image-server/observations/LAT20LONG10202001131.png",
                "timestamp": 2020013,
                "target_id": 1
            },
            1: {
                "id": 1,
                "image_url": "http://image-server/observations/LAT20LONG10202001142.png",
                "timestamp": 2020014,
                "target_id": 1
            },
            2: {
                "id": 2,
                "image_url": "http://image-server/observations/LAT20LONG10202001153.png",
                "timestamp": 2020015,
                "target_id": 1
            },
        }

Or a KML file
