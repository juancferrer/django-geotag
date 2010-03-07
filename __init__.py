from django.dispatch import Signal
from django.utils.translation import ugettext as _

from managers import LocationDescriptor
from models import *
from signals import location_post_registration

VERSION = (0, 1, 'alpha')

registry = []

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model with the same 
    location type more than once.
    """
    pass

class AttributeAlreadyExists(Exception):
    """
    An attempt was made to register a model but the location 
    attribute already exists.
    """
    pass

class InvalidLocationType(Exception):
    """
    An attempt was made to register a model but the location 
    type is not valid.
    """
    pass

def register(model, name='location', type='point'):
    """
    Sets the given model class up for working with locations.
    """
    if type not in ('point', 'poly', 'multi_point', 'multi_poly',):
        raise InvalidLocationType, "Invalid location type"

    if type == 'poly':
        location_model = PolyLocation
    elif type == 'multi_point':
        location_model = MultiPointLocation
    elif type == 'multi_poly':
        location_model = MultiPolyLocation
    else:
        location_model = PointLocation

    if (model, location_model) in registry:
        raise AlreadyRegistered(
                _('The model %s has already been registered with a %s.') %
                        (model.__name__, location_model.__name__,)
            )

    if hasattr(model, name):
        raise AttributeAlreadyExists(
                 _('The model %s already has an attribute %s') %
                         (model.__name__, name)
            )

    #Register
    registry.append((model, location_model, name))

    # Add location descriptor
    setattr(model, name,
            LocationDescriptor(location_model = location_model)
            )

    #Send the signal that a model was registered with the geotag app
    location_post_registration.send(sender= None, model= model,
            location_model = location_model, name = name
            )
