Django Geotag
=================

A tagging application in the spirit of ``'django-tagging'``.
It allows to tag any django model with any number of Geodjango geometry fields
such as PointField, PolygonField, etc...

Installation
------------
For now, just place the ``'geotag'`` directory into your django project
directory.

Configuration and Usage
-----------------------

Add ``'geotag'`` to your ``INSTALLED_APPS``.

Register your models with the geotag app to add any number of
geometric field types to your models.

Example::

    import geotag

    class Building(models.Model):
        ...
    geotag.register(Building)

    class Antenna(models.Model):
        type = models.CharField(max_length=50)
    geotag.register(Antenna, name='site')
    geotag.register(Antenna, type='poly', name='service_area')

The only required argument for the ``'geotag.register'`` function is the
django model class. 

The other arguments are ``'type'`` and ``'name'``.

``'type'`` can be any of the following, defaults to ``'point'``:

* ``'point'`` for a ``PointField``
* ``'multi_point'`` for a ``MultiPointField``
* ``'poly'`` for a ``PolygonField``
* ``'multi_poly`` for a ``MultiPolygonField``

``'name'`` will become the name of the attribute for the geometry field.
Defaults to ``'location'``

Then in the django shell

::

 >>>from django.contrib.gis.geos import Point, Polygon
 >>>from models import Building, Antenna
 >>>building = Building.objects.create()
 >>>building.location

 >>>building.location = Point(0,0)
 <PointLocation: SRID=4326;POINT (0.0000000000000000 0.0000000000000000)>
 >>>antenna = Antenna.objects.create()
 >>>antenna.site = Point(0,0)
 <PointLocation: SRID=4326;POINT (0.0000000000000000 0.0000000000000000)>
 >>>antenna.service_area = Polygon(((0,0),(0,10),(10,10),(0,10),(0,0)))
 <PolyLocation: SRID=4326;POLYGON ((0.0000000000000000 0.0000000000000000, 0.0000000000000000 10.0000000000000000, 10.0000000000000000 10.0000000000000000, 0.0000000000000000 10.0000000000000000, 0.0000000000000000 0.0000000000000000))>

To Do
-----

* TESTS!
* Admin interface
* setuptools packaging
