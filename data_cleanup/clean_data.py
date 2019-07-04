"""
A data clean up module
"""
import django.apps


def get_all_models():
    """
    Fetches all the models in the system
    """
    all_models = django.apps.apps.get_models()
    return all_models


def get_model_fields(model_class):
    """
    Get all the fields in  a model and returns their type.
    """

def compare_values(model_class, operator, value):
    """
    Get all data from a model matching a certain criteria.
    """
