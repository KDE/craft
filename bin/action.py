#
# prelimary implementation for standardized command line parameter parsing and action handling
#
# (c) copyright 2011 Ralf Habacker <ralf.habacker@freenet.de>
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
    defined = False
    def __init__( self, actionString, helpString ):
        if type( actionString ) == list:
            self.destString = actionString[0]
            self.actionString = actionString
        else:
            self.destString = actionString
            self.actionString = [actionString]

        self.helpString = helpString

    def string( self ):
        return self.actionString

    def insertIntoParser( self, parser ):
        names = []
        for s in self.actionString:
            if len(s) == 1:
                names.append( '-%s' % s )
            else:
                names.append( '--%s' % s )
        # @todo do not know how to add more then one name
        # using names as first parameter fails with ValueError: dest supplied twice for positional argument
        parser.add_argument( names[0], default=False, action='store_true', help=m18n(self.helpString), dest=self.destString)
        return True

class ActionFetch( ActionBase ):
    """defines the fetch action"""
    def __init__( self ):
        ActionBase.__init__( self, 'fetch',
            'retrieve package sources either from files, archives or version control systems.' )

class ActionUnpack( ActionBase ):
    """defines the unpack action"""
    def __init__( self ):
        ActionBase.__init__( self, 'unpack',
            'unpack package sources and make up the build directory' )

class ActionCompile( ActionBase ):
    """defines the compile action"""
    def __init__( self ):
        ActionBase.__init__( self, 'compile', 'configure and make the package' )

class ActionConfigure( ActionBase ):
    """defines the configure action"""
    def __init__( self ):
        ActionBase.__init__( self, 'configure', 'configure the package' )

class ActionMake( ActionBase ):
    """defines the make action"""
    def __init__( self ):
        ActionBase.__init__( self, 'make', 'run compiler and buildsystem specific make tool' )

class ActionInstall( ActionBase ):
    """defines the install action"""
    def __init__( self ):
        ActionBase.__init__( self, 'install', 'install the generated files into the image \
            directory of the related package' )

class ActionMerge( ActionBase ):
    """defines the merge action"""
    def __init__( self ):
        ActionBase.__init__( self, 'qmerge', 'merge the image directory into the merge root' )

class ActionUnMerge( ActionBase ):
    """defines the unmerge action"""
    def __init__( self ):
        ActionBase.__init__( self, 'unmerge', 'uninstalls a package from the merge root \
            (requires a working manifest directory). Unmerge only delete unmodified files by default. \
            You may use the -f or --force option to let unmerge delete all files unconditional.' )

class ActionManifest( ActionBase ):
    """defines the manifest action"""
    def __init__( self ):
        ActionBase.__init__( self, 'manifest', 'creates the files contained in the manifest dir' )

class ActionTest( ActionBase ):
    """defines the test action"""
    def __init__( self ):
        ActionBase.__init__( self, 'test', 'run the unittests if they are present' )

class ActionPackage( ActionBase ):
    """defines the package action"""
    def __init__( self ):
        ActionBase.__init__( self, 'package', 'create an installable package from the image directory' )

class ActionPrintRevision( ActionBase ):
    """defines the print revision action"""
    def __init__( self ):
        ActionBase.__init__( self, 'print-revision', 'print the revision that the source repository \
            of this package currently has or nothing if there is no repository' )

class ActionPrintTargets( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'print-targets', 'print all the different targets one package \
            can contain: different releases might have different tags that are build as targets of a \
            package. As an example: You could build the latest amarok sources with the target \'svnHEAD\' \
            the previous \'1.80\' release would be contained as target \'1.80\'.' )

class ActionDumpDependencies( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, ['dumpdeps','dump-deps'], 'print all the different targets one \
            package can contain: different releases might have different tags that are build as targets \
            of a package. As an example: You could build the latest amarok sources with the target \
            \'svnHEAD\' the previous \'1.80\' release would be contained as target \'1.80\'.' )

class ActionCleanAllBuilds( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'cleanallbuilds', 'clean complete build directory' )

class ActionCleanBuild( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'cleanbuild', 'clean build directory and image directories \
            for the specified package' )

class ActionCheckDigest( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'checkdigest', 'check digest for the specified package. \
            If no digest is available calculate and print digests' )

class ActionCleanImage( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'cleanimage', 'clean image directory for the specified \
            package and target' )

class ActionCreatePatch( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'createpatch', 'create source patch file for the specific \
            package based on the original archive file or checkout revision of \
            the used software revision control system' )

class ActionDisableBuildHost( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'disable-buildhost', 'disable the building for the host' )

class ActionDisableBuildTarget( ActionBase ):
    """defines the print targets action"""
    def __init__( self ):
        ActionBase.__init__( self, 'disable-buildtarget', 'disable the building for the target' )

class ActionInstallDependencies( ActionBase ):
    """defines the install dependencies action"""
    def __init__( self ):
        ActionBase.__init__( self, 'install-deps', 'fetch and install all required \
            dependencies for the specified package' )
            
#template
#class Action( ActionBase ):
#    """defines the print targets action"""
#    def __init__( self ):
#        ActionBase.__init__( self, '', '' )

__init__()

# for debugging
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='package build tool')
    for a in actionClasses:
        a.insertIntoParser( p )
    args = p.parse_args()
    print args

