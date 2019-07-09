from django.conf import settings


def global_settings(request):
    """
    Inject particular settings in request to be accessed in templates
    :param request:
    :return:
    """
    return {
        'OFFLINE_MODE_CAPABILITY_ENABLED': settings.OFFLINE_MODE_CAPABILITY_ENABLED
    }
