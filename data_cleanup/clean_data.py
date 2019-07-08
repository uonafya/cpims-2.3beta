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


def get_model_fields():
    """
    Get all the fields in  a model and returns their type.
    """
    all_models =  get_all_models()
    models_data = {}
    for model in all_models:
        fields = model._meta.fields
        field_data = []
        for field in fields:
            field_data.append(
                {
                    "field_name": str(field.name),
                    "field_type": str(field.__class__.__name__)
                }
            )
        models_data[str(model)] = field_data
    return models_data
    

def compare_values(model_class, operator, value):
    """
    Get all data from a model matching a certain criteria.
    """
