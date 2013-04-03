## add some default functionality for KDE packages.
import utils
from portage import rootDirectories
from os.path import dirname as dn, join as j, normcase, relpath, sep

def __kdepath(name):
    """ return the path of the kde category directory. If multiple portages are used,
        return the correct one. """
    if name:
        rootDirFound = False
        name = normcase(name)
        for dirname in rootDirectories():
            dirname = normcase(dirname)
            if name.startswith(dirname):
                name = j(dirname, relpath(name, dirname).split(sep)[0])
                rootDirFound = True
                break
        # this is hopefully a fallback solution, if not - no idea
        if not rootDirFound: name = dn(dn(name))
    return name

kdepath = __kdepath(utils.getCallerFilename())

def __kdebranch():
    return open(j(kdepath, 'kdebranch')).read()

kdebranch = __kdebranch()
    
def __kdeversion():
    return open(j(kdepath, 'kdeversion')).read() + "."

kdeversion = __kdeversion()


