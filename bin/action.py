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

actionClasses = []


def m18n(s):
    """prelimary function for internationalization support"""
    return s

def __init__():
    if not ActionBase.defined:
        for v in globals().values():
            if type(v).__name__ == 'classobj' and v.__name__ != 'ActionBase':
                action = v()
                actionClasses.append( action )

class ActionBase:
    """this class defines available actions"""
    defined = None

    def argName(self):
        return self.__class__.__name__[6:].lower().replace('_','-')

    def destString(self):
        return self.argName()

    def insertIntoParser( self, parser ):
        helpString = self.__class__.__doc__
        print self.argName(), self.destString(), helpString
        parser.add_argument( '--'+self.argName(), default=False, action='store_true', help=m18n(helpString), dest=self.destString())

class ActionFetch( ActionBase ):
    """retrieve package sources either from files, archives or version control systems."""

class ActionUnpack( ActionBase ):
    """unpack package sources and make up the build directory"""

class ActionCompile( ActionBase ):
    """configure and make the package"""

class ActionConfigure( ActionBase ):
    """configure the package"""

class ActionMake( ActionBase ):
    """run compiler and buildsystem specific make tool"""

class ActionInstall( ActionBase ):
    """install the generated files into the image 
       directory of the related package"""

class ActionMerge( ActionBase ):
    """merge the image directory into the merge root"""

class ActionUnmerge( ActionBase ):
    """uninstalls a package from the merge root
(requires a working manifest directory). Unmerge only delete unmodified files by default.
You may use the -f or --force option to let unmerge delete all files unconditional."""

class ActionManifest( ActionBase ):
    """creates the files contained in the manifest dir"""

class ActionTest( ActionBase ):
    """run the unittests if they are present"""

class ActionPackage( ActionBase ):
    """create an installable package from the image directory"""

class ActionPrint_revision( ActionBase ):
    """print the revision that the source repository
of this package currently has or nothing if there is no repository"""

class ActionPrint_targets( ActionBase ):
    """print all the different targets one package
            can contain: different releases might have different tags that are build as targets of a
            package. As an example: You could build the latest amarok sources with the target 'svnHEAD'
            the previous '1.80' release would be contained as target '1.80'."""

class ActionDumpdeps( ActionBase ):
    """alternative name for dump-deps"""

class ActionDump_deps(ActionDumpdeps):
    """print all the different targets one
            package can contain: different releases might have different tags that are build as targets
            of a package. As an example: You could build the latest amarok sources with the target
            'svnHEAD' the previous '1.80' release would be contained as target '1.80'."""
    def destString(self):
        return 'dumpdeps'

class ActionCleanallbuilds( ActionBase ):
    """clean complete build directory"""

class ActionCleanbuild( ActionBase ):
    """clean build directory and image directories for the specified package"""

class ActionCheckdigest( ActionBase ):
    """check digest for the specified package.
            If no digest is available calculate and print digests"""

class ActionCleanimage( ActionBase ):
    """clean image directory for the specified
            package and target"""

class ActionCreatepatch( ActionBase ):
    """create source patch file for the specific
            package based on the original archive file or checkout revision of
            the used software revision control system"""

class ActionDisableBuildhost( ActionBase ):
    """disable the building for the host"""

class ActionDisableBuild_target( ActionBase ):
    """disable the building for the target"""

class ActionInstall_deps( ActionBase ):
    """fetch and install all required 
            dependencies for the specified package"""
            
__init__()

# for debugging
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='package build tool')
    for a in actionClasses:
        a.insertIntoParser( p )
    args = p.parse_args()
    print args

