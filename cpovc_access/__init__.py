"""This is for versioning."""

default_app_config = 'cpovc_access.apps.AccessAppConfig'
__version__ = '1.5.0'


def get_version():
    """Return version."""
    return __version__


class BasePolicy(object):
    """Initialize base policy."""

    def __init__(self, **kwargs):
        """Policy configuration happens at init."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
