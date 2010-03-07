from django.dispatch import Signal

location_post_registration=Signal(
        providing_args=["model", "location_model", "name"]
        )

