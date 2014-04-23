## add some default functionality for KDE packages.
from os.path import dirname as dn, join as j, normcase, relpath, sep, exists

import utils
from portage import rootDirectories


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

def __readFile(name):
    path = j(kdepath, name)
    out = None
    if exists(path):
        f = open(path)
        out = f.read()
        f.close()
    return out
    
def __kdebranch():
    return __readFile('kdebranch')
 
    
kdebranch = __kdebranch()
    
def __kdeversion():
    out = __readFile('kdeversion')
    if out:
        out += "."
    return out

kdeversion = __kdeversion()


def setKDEPath(name):
    global kdepath    
    global kdebranch    
    global kdeversion 
    kdepath = name
    kdebranch = __kdebranch()
    kdeversion = __kdeversion()



