"""
Custom managers for Django models registered with the geotag
application.
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as geomodels

class ModelLocationManager(geomodels.GeoManager):
    """
    A manager for retrieving the location for a particular model.
    """
    def get_query_set(self):
        raise NotImplementedError, "ModelLocationManager.get_query_set() not implemented"
#        ctype = ContentType.objects.get_for_model(self.model)
#        return Location.objects.filter(content_type__pk=ctype.pk)

class LocationDescriptor(object):
    """
    A descriptor which provides access to a ``ModelLocationManager`` for
    model classes and simple retrieval, updating and deletion of locations
    for model instances.
    """
    def __init__(self, *args, **kwargs):
        self.location = kwargs.get('location_model')

    def __get__(self, instance, owner):
        if not instance:
            location_manager = ModelLocationManager()
            location_manager.model = owner
            return location_manager
        else:
            return self.location.objects.get_for_object(instance)

    def __set__(self, instance, value):
        self.location.objects.set_location(instance, value)

    def __delete__(self, instance):
        self.location.objects.delete_location(instance, None)
