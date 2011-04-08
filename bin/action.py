#!/usr/bin/env python2.7
#
# prelimary implementation for standardized command line parameter parsing and action handling
#
# (c) copyright 2011 Ralf Habacker <ralf.habacker@freenet.de>
# (c) copyright 2011 Wolfgang Rohdewald <wolfgang@rohdewald.de>
#
# @TODO review help texts
#
#
import sys, argparse

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
        argClasses = []
        for v in globals().values():
            if hasattr(v, "__mro__"):
                if v.__name__.endswith('Arg'):
                    argClass = v()
                    argClasses.append(argClass)
    ArgBase.defined = sorted(argClasses, key=lambda x: x.number)
    for argClass in ArgBase.defined:
        argClass.setup()

class ArgBase(object):
    """this class defines available actions"""
    __metaclass__ = AutoNumberingType
    defined = []
    argGroupName = None
    argGroups = {}
    parser = None
    alternativeNames = []
    classes = {}

    def setup(self):
        """we do not want to do this in __init__ because invocation order matters
           otherwise the groups would not be ordered as they appear in this file"""
        self.argValue = None
        if not ArgBase.parser:
            ArgBase.parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description="""
emerge [[ command and flags ] [ TARGET ]
        [ command and flags ] [ TARGET ]
        ... ]

where TARGET can be of the form:
    category
    package
    category/package

Emerge is a tool for building KDE-related software under Windows. emerge
automates it, looks for the dependencies and fetches them automatically.
Some options should be used with extreme caution since they will
make your kde installation unusable in 999 out of 1000 cases.""")
        argGroupName = self.argGroupName
        if argGroupName not in self.argGroups:
            self.argGroups[argGroupName] = self.parser.add_argument_group(argGroupName)
        self.argGroup = self.argGroups[argGroupName]
        self.helpString = self.__class__.__doc__
        self.argName = self.__class__.__name__[:-3].lower().replace('_','-')
        self.classes[self.argName] = self

    def argStrings(self):
        result = ['--' + self.argName]
        for name in self.alternativeNames:
            if len(name) == 1:
                result.insert(0, '-' + name)
            else:
                result.append('--' + name)
        return result

    def insertIntoParser( self ):
        """default for parameters without value"""
        self.argGroup.add_argument(*self.argStrings(),
                action='store_true', help=m18n(self.helpString), dest=self.argName)

class CommandArgBase(ArgBase):
    """for command arguments"""

class GeneralCommandArgBase(CommandArgBase):
    """for non package related arguments without value"""
    argGroupName = "Commands without packagename"

class PackageCommandArgBase(CommandArgBase):
    """for package related arguments with package value"""
    argGroupName = "Commands (must have a packagename). Only one such command is allowed"

    def insertIntoParser( self ):
        self.argGroup.add_argument(*self.argStrings(), default=False,
                help=m18n(self.helpString),
                metavar='TARGET',
                dest=self.argName)

class FlagArgBase(ArgBase):
    """for flag arguments"""
    argGroupName = "Flags"

class InternalArgBase(object):
    """mixin for internal arguments. Use this as first parent class"""
    argGroupName = "Internal options or options that aren't fully implemented yet"

class ObsoleteArgBase(object):
    """mixin for obsolete arguments. Use this as first parent class"""
    argGroupName = "Obsolete"

class CleanallbuildsArg( GeneralCommandArgBase ):
    """clean complete build directory"""

class FetchArg( PackageCommandArgBase ):
    """retrieve package sources either from files,
       archives or version control systems."""

class UnpackArg( PackageCommandArgBase ):
    """unpack package sources and make up the build directory"""

class CompileArg( PackageCommandArgBase ):
    """configure and make the package"""

class ConfigureArg( PackageCommandArgBase ):
    """configure the package"""

class MakeArg( PackageCommandArgBase ):
    """run compiler and buildsystem specific make tool"""

class InstallArg( PackageCommandArgBase ):
    """install the generated files into the image
       directory of the related package"""

class MergeArg( PackageCommandArgBase ):
    """merge the image directory into the merge root"""

class UnmergeArg( PackageCommandArgBase ):
    """uninstalls a package from the merge root
       (requires a working manifest directory).
       Unmerge only delete unmodified files by default.
       You may use the -f or --force option to let unmerge
       delete all files unconditional."""

class ManifestArg( PackageCommandArgBase ):
    """creates the files contained in the manifest dir"""

class TestArg( PackageCommandArgBase ):
    """run the unittests if they are present"""

class PackageArg( PackageCommandArgBase ):
    """create an installable package from the image directory"""


class AllArg( PackageCommandArgBase ):
    """perform all required actions to build a runable package, which are 
       --fetch, --unpack, --compile, --install, --manifest and --qmerge"""

class Full_packageArg( PackageCommandArgBase ):
    """perform all required actions to build a binary package, which are 
       --fetch, --unpack, --compile, --install and --package"""

class Print_revisionArg( PackageCommandArgBase ):
    """print the revision that the source repository
       of this package currently has or nothing if there is no repository"""

class Print_targetsArg( PackageCommandArgBase ):
    """print all the different targets one package
       can contain: different releases might have different tags that are build as targets of a
       package. As an example: You could build the latest amarok sources with the target 'svnHEAD'
       the previous '1.80' release would be contained as target '1.80'."""

class Dump_depsArg( PackageCommandArgBase ):
    """print all the different targets one
       package can contain: different releases might have different tags that are build as targets
       of a package. As an example: You could build the latest amarok sources with the target
       'svnHEAD' the previous '1.80' release would be contained as target '1.80'."""
    alternativeNames = ['dumpdeps']

class CleanbuildArg( PackageCommandArgBase ):
    """clean build directory and image directories for the specified package"""

class CheckdigestArg( PackageCommandArgBase ):
    """check digest for the specified package.
       If no digest is available calculate and print digests"""

class CleanimageArg( PackageCommandArgBase ):
    """clean image directory for the specified
       package and target"""

class CreatepatchArg( PackageCommandArgBase ):
    """create source patch file for the specific
       package based on the original archive file or checkout revision of
       the used software revision control system"""

class DisableBuildhostArg( FlagArgBase ):
    """disable the building for the host"""

class DisableBuild_targetArg( FlagArgBase ):
    """disable the building for the target"""

class Install_depsArg( PackageCommandArgBase ):
    """fetch and install all required
       dependencies for the specified package"""

class Version_dirArg(ObsoleteArgBase, PackageCommandArgBase):
    """whatever this does"""

class ContinueArg(InternalArgBase, FlagArgBase):
    """after having done the package command, continue with
       the next commands this package normally gets"""
    alternativeNames = ['c']

__init__()

# for debugging
if __name__ == "__main__":
    for a in ArgBase.defined:
        a.insertIntoParser()
    args = ArgBase.parser.parse_args()

    # put the values into their respective classes:
    for name in args.__dict__:
        value = args.__dict__[name]
        ArgBase.classes[name].argValue = value
        if not value == False:
            print name, args.__dict__[name]
    if len([x for x in ArgBase.classes.values()
            if isinstance(x, PackageCommandArgBase) and x.argValue]) > 1:
        print 'only one command with PACKAGE may be given'
        sys.exit(2)
    # run action 
