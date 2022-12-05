"""Utility functions"""

from django.db.models import Model


def get_field(name: str, model: Model):
    """
    Get a field by name from a model.

    parmeters:
    The name of the field which will be retrieved.
    The model that contains the field.
    """
    return model._meta.get_field(name)
