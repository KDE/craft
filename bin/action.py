#!/usr/bin/env python2.7
#
# prelimary implementation for standardized command line parameter parsing and action handling
#
# (c) copyright 2011 Ralf Habacker <ralf.habacker@freenet.de>
# (c) copyright 2011 Wolfgang Rohdewald <wolfgang@rohdewald.de>
#
# @TODO review help texts 
# @TODO fix parameter ordering (order of class list below)
#
#
import argparse

def m18n(s):
    """prelimary function for internationalization support"""
    return s

classNumber = 0        # to be used by AutoNumberingType

class AutoNumberingType(type):
    """all classes with this as metaclass get an attribute 'number'
       which increases by order of class definition (order in this file)"""
    def __init__(cls, name, bases, attrs):
        global classNumber
        classNumber = classNumber + 1
        setattr(cls,'number', classNumber)
 
def __init__():
    if not ArgBase.defined:
        actionClasses = []
        for v in globals().values():
            if hasattr(v, "__mro__"):
                if len(v.__mro__) > 2 and  v.__mro__[-2] == ArgBase:
                    action = v()
                    actionClasses.append(action)
    ArgBase.defined = sorted(actionClasses, key=lambda x: x.number)
    

class ArgBase(object):
    """this class defines available actions"""
    __metaclass__ = AutoNumberingType
    defined = []

    def argName(self):
        return self.__class__.__name__[6:].lower().replace('_','-')

    def destString(self):
        return self.argName()

    def insertIntoParser( self, parser ):
        helpString = self.__class__.__doc__
        parser.add_argument( '--'+self.argName(), default=False, action='store_true', help=m18n(helpString), dest=self.destString())

class ActionFetch( ArgBase ):
    """retrieve package sources either from files, archives or version control systems."""

class ActionUnpack( ArgBase ):
    """unpack package sources and make up the build directory"""

class ActionCompile( ArgBase ):
    """configure and make the package"""

class ActionConfigure( ArgBase ):
    """configure the package"""

class ActionMake( ArgBase ):
    """run compiler and buildsystem specific make tool"""

class ActionInstall( ArgBase ):
    """install the generated files into the image 
       directory of the related package"""

class ActionMerge( ArgBase ):
    """merge the image directory into the merge root"""

class ActionUnmerge( ArgBase ):
    """uninstalls a package from the merge root
(requires a working manifest directory). Unmerge only delete unmodified files by default.
You may use the -f or --force option to let unmerge delete all files unconditional."""

class ActionManifest( ArgBase ):
    """creates the files contained in the manifest dir"""

class ActionTest( ArgBase ):
    """run the unittests if they are present"""

class ActionPackage( ArgBase ):
    """create an installable package from the image directory"""

class ActionPrint_revision( ArgBase ):
    """print the revision that the source repository
of this package currently has or nothing if there is no repository"""

class ActionPrint_targets( ArgBase ):
    """print all the different targets one package
            can contain: different releases might have different tags that are build as targets of a
            package. As an example: You could build the latest amarok sources with the target 'svnHEAD'
            the previous '1.80' release would be contained as target '1.80'."""

class ActionDumpdeps( ArgBase ):
    """alternative name for dump-deps"""

class ActionDump_deps(ActionDumpdeps):
    """print all the different targets one
            package can contain: different releases might have different tags that are build as targets
            of a package. As an example: You could build the latest amarok sources with the target
            'svnHEAD' the previous '1.80' release would be contained as target '1.80'."""
    def destString(self):
        return 'dumpdeps'

class ActionCleanallbuilds( ArgBase ):
    """clean complete build directory"""

class ActionCleanbuild( ArgBase ):
    """clean build directory and image directories for the specified package"""

class ActionCheckdigest( ArgBase ):
    """check digest for the specified package.
            If no digest is available calculate and print digests"""

class ActionCleanimage( ArgBase ):
    """clean image directory for the specified
            package and target"""

class ActionCreatepatch( ArgBase ):
    """create source patch file for the specific
            package based on the original archive file or checkout revision of
            the used software revision control system"""

class ActionDisableBuildhost( ArgBase ):
    """disable the building for the host"""

class ActionDisableBuild_target( ArgBase ):
    """disable the building for the target"""

class ActionInstall_deps( ArgBase ):
    """fetch and install all required 
            dependencies for the specified package"""
            
__init__()

# for debugging
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='package build tool')
    for a in ArgBase.defined:
        a.insertIntoParser( p )
    args = p.parse_args()
    print args

