## add some default functionality for KDE packages.
import utils
from portage import rootDirectories
from os.path import dirname as dn, join as j, sep

def __kdepath(name):
    """ return the path of the kde category directory. If multiple portages are used,
        return the correct one. """
    rootDirFound = False
    for dirname in rootDirectories():
        if name.startswith(dirname):
            if not dirname.endswith(sep): dirname = dirname + sep
            name = dirname + name.replace(dirname, "").split(sep)[0]
            rootDirFound = True
            break
    # this is hopefully a fallback solution, if not - no idea
    if not rootDirFound: name = sep.join(name.split(sep)[:-2])
    return name

kdepath = __kdepath(utils.getCallerFilename())

def __kdebranch():
    return open(j(kdepath, 'kdebranch')).read()

kdebranch = __kdebranch()
    
def __kdeversion():
    return open(j(kdepath, 'kdeversion')).read() + "."

kdeversion = __kdeversion()


