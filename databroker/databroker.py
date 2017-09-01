# This module exists only for backward-compatiblity.
# Older versions of databroker created a singleton instance of Broker at
# import time. Current versions of databroker support multiple instances of
# Broker, created interactively after import.

# This module look for a specially-named configuration file and generates a
# special instance of Broker to avoid breaking old user code.

from ._core import Broker, lookup_config, SPECIAL_NAME
from ._core import get_fields  # unused, but here for API compat
from functools import wraps
import os
import six
from warnings import warn

if six.PY2:
    FileNotFoundError = IOError


def deprecate(f):
    @wraps(f)
    def inner(*args, **kwargs):
        name = getattr(f, '__name__', '')  # works on py3.5+
        warn("This function {} is deprecated. Use a method on Broker instead."
            "".format(name))
        return f(*args, **kwargs)
    return inner


try:
    config = lookup_config(SPECIAL_NAME)
except FileNotFoundError:
    # No config was provided for back-compatibility so there we be no
    # pre-built Broker instance.
    pass
else:
    # Don't allow any errors generated by loading this instance to escape and
    # make databroker un-importable.
    try:
        DataBroker = Broker.from_config(config)
    except Exception as exc:
        warn("There was a error loading {!r}: {!r}".format(SPECIAL_NAME, exc))
    else:
        get_events = deprecate(DataBroker.get_events)
        get_table = deprecate(DataBroker.get_table)
        get_images = deprecate(DataBroker.get_images)
        restream = deprecate(DataBroker.restream)
        stream = deprecate(DataBroker.stream)
        process = deprecate(DataBroker.process)
        fill_event = deprecate(DataBroker.fill_event)
