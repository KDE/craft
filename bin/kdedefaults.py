## add some default functionality for KDE packages.
import utils
from portage import rootDirs
from os.path import dirname as dn, join as j

def __kdepath(name):
    for dirname in rootDirs():
        if name.startswith(dirname):
            name.replace(dirname)
            break
    return j(dn(name), '')

kdepath = __kdepath(utils.getCallerFilename())

def __kdebranch():
    return open(j(kdepath, 'kdebranch')).read()

kdebranch = __kdebranch()
    
def __kdeversion():
    return open(j(kdepath, 'kdeversion')).read() + "."

kdeversion = __kdeversion()


