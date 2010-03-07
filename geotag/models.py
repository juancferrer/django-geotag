"""
Models and managers for geotag.
"""
from django.db import  models
from django.db.models.signals import pre_delete
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as geomodels
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from signals import location_post_registration
import geotag

############
# Managers #
############

class LocationManager(geomodels.GeoManager):
    # http://docs.djangoproject.com/en/dev/topics/db/managers/#controlling-automatic-manager-types
    use_for_related_fields = True

    def set_location(self, obj, location):
        """
        Sets the location for the given object
        """
        ctype = ContentType.objects.get_for_model(obj)
        #Get the object and update, or make a new one
        try:
            inst=self.get(content_type=ctype, object_id=obj.id)
            inst.location = location
            inst.save()
        except ObjectDoesNotExist:
            self.create(content_type=ctype,object_id=obj.id,location=location)

    def delete_location(self, obj):
        """
        Deletes the location for the given object
        """
        ctype = ContentType.objects.get_for_model(obj)
        self.filter(content_type = ctype, object_id=obj.id).delete()

    def get_for_object(self, obj):
        """
        Returns the location for the given object
        """
        ctype = ContentType.objects.get_for_model(obj)
        try:
            return self.get(content_type=ctype, object_id=obj.id)
        except ObjectDoesNotExist:
            return None

##########
# Models #
##########

class AbstractLocation(geomodels.Model):
    """
    Abstract base class for PointLocation and PolyLocation
    """
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), )
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = LocationManager()

    class Meta:
        abstract = True
        ordering = ('location',)
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __unicode__(self):
        return self.location.ewkt #Derived concrete classes have a location


class PointLocation(AbstractLocation):
    """
    A point location
    """
    location = geomodels.PointField(_('point'),  srid=4326)
    
class MultiPointLocation(AbstractLocation):
    """
    A multi-point location
    """
    location = geomodels.MultiPointField(_('multi-point'), )

class PolyLocation(AbstractLocation):
    """
    A polygon location
    """
    location = geomodels.PolygonField(_('polygon'), )

class MultiPolyLocation(AbstractLocation):
    """
    A multi-polygon location
    """
    location = geomodels.MultiPolygonField(_('multi-polygon'), )

#################
# Catch signals #
################

#Delete the location when a model is about to be deleted
def delete_location_for_model(sender, instance, **kwargs):
    for model, location_model, name in geotag.registry:
        if model == sender:
            delattr(instance, name)

def connect_delete_model(sender, model, location_model, name, **kwargs):
    pre_delete.connect(delete_location_for_model, sender=model)

#When a model is registered, connect to the pre_delete signal for that model
location_post_registration.connect(connect_delete_model)
