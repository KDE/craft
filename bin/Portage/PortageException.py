from Portage.CraftPackageObject import CraftPackageObject


class PortageException(Exception, CraftPackageObject):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)
        CraftPackageObject.__init__(self, package.path)
        self.exception = exception

    def __str__(self):
        return f"{CraftPackageObject.__str__(self)} failed: {Exception.__str__(self)}"
