import Notifier.NotificationInterface
import importlib

_NOTIFICATION_BACKENDS = None
def load(modules):
    global _NOTIFICATION_BACKENDS;
    if _NOTIFICATION_BACKENDS == None:
        _NOTIFICATION_BACKENDS = dict()
        for backend in modules:
            backend = getattr(importlib.import_module("Notifier.Backends.%s" % backend),backend)()  
            _NOTIFICATION_BACKENDS[backend.name] = backend
    return _NOTIFICATION_BACKENDS
 

