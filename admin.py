from django.contrib.gis import admin
from models import *

admin.site.register(PointLocation, admin.OSMGeoAdmin)
admin.site.register(MultiPointLocation, admin.OSMGeoAdmin)
admin.site.register(PolyLocation, admin.OSMGeoAdmin)
admin.site.register(MultiPolyLocation, admin.OSMGeoAdmin)

