#!/usr/bin/env python2.7
#
# prelimary implementation for standardized command line parameter parsing and action handling
#
# (c) copyright 2011 Ralf Habacker <ralf.habacker@freenet.de>
# (c) copyright 2011 Wolfgang Rohdewald <wolfgang@rohdewald.de>
#
# @TODO review help texts
#

import sys, argparse

import portage

def m18n(s):
    """prelimary function for internationalization support"""
    return s

classNumber = 0        # to be used by AutoNumberingType

class AutoNumberingType(type):
    """all classes with this as metaclass get an attribute 'number'
       which increases by order of class definition (order in this file)"""
    def __init__(cls, name, bases, attrs):
        global classNumber
        classNumber += 1
        setattr(cls, 'number', classNumber)

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
    classByName = {}
    classByType = {}

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
        self.classByName[self.argName] = self
        self.classByType[self.__class__] = self
        self.insertIntoParser()

    def argStrings(self):
        args = [self.argName]
        args += self.alternativeNames
        result = []
        for name in args:
            if len(name) < 3:
                result.append('-' + name)
            else:
                result.append('--' + name)
        return result

    def insertIntoParser( self ):
        """default for parameters without value"""
        self.argGroup.add_argument(*self.argStrings(),
                action='store_true', help=m18n(self.helpString), dest=self.argName)

    def execArg(self):
        """what the command should do"""

    def __str__(self):
        """used for print"""
        return self.__class__.__name__ + ' argValue:%s' % self.argValue

class CommandArgBase(ArgBase):
    """for command arguments"""
    def expand(self):
        """a meta command may expand itself into several commands"""
        return [self.__class__]

class GeneralCommandArgBase(CommandArgBase):
    """for non package related arguments without value"""
    argGroupName = "Commands without target"

class PackageCommandArgBase(CommandArgBase):
    """for package related arguments with package value"""
    argGroupName = "Commands (must have a target). Only one such command is allowed"

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

class Print_installableArg(GeneralCommandArgBase):
    """list packages that can be installed"""
    def execArg(self):
        portage.printInstallables()

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

class QmergeArg( PackageCommandArgBase ):
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
    def expand(self):
        return [FetchArg, UnpackArg, ConfigureArg, MakeArg, InstallArg, ManifestArg, QmergeArg]

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

class DumpDepsArg( PackageCommandArgBase ):
    """print all the different targets one
       package can contain: different releases might have different tags that are build as targets
       of a package. As an example: You could build the latest amarok sources with the target
       'svnHEAD' the previous '1.80' release would be contained as target '1.80'."""
    #alternativeNames = ['dump-deps']

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

class ContinueArg(FlagArgBase):
    """after having done the package command, continue with
       the next commands this package normally gets"""
    alternativeNames = ['c']

class IArg(FlagArgBase):
    """ignore install: using this option will install a package over an
       existing install. This can be useful if you want to check some
       new code and your last build isn't that old."""
    #alternativeNames = ['ignore-install']

class PArg(FlagArgBase):
    """probing: emerge will only look which files it has to build
       according to the list of installed files and according to the
       dependencies of the package."""
    alternativeNames = ['probe']

class QArg(FlagArgBase):
    """there should be no output - The verbose level should be 0"""
    #alternativeNames = ['quiet']

class TArg(FlagArgBase):
    """if used on an KDE target it will override the environment
        variable and build the target with -DKDE_BUILD_TESTS=ON"""
    #alternativeNames = ['test']

class VArg(FlagArgBase):
    """increases the verbose level of emerge. Default is 1.
       verbose level 1 contains some notes from emerge, all output of
       cmake, make and other programs that are used. verbose level 2
       adds an option VERBOSE=1 to make and emerge is more verbose
       highest level is verbose level 3."""
    #alternativeNames = ['verbose']

class ZArg(FlagArgBase):
    """if packages from version control system sources are installed,
       it marks them as out of date and rebuilds them (tags are not
       marked as out of date)."""
    #alternativeNames = ['outdate']

class SZArg(FlagArgBase):
    """similar to -z, only that it acts only on the last package, and
       works as normal on the rest."""
    #alternativeNames = ['outdate-last']

class NoCleanArg(FlagArgBase):
    """this option will try to use an existing build directory. Please
       handle this option with care - it will possibly break if the
       directory isn't existing."""
       
class OfflineArg(FlagArgBase):
    """do not try to connect to the internet: KDE packages will try to
       use an existing source tree and other packages would try to use
       existing packages in the download directory. If that doesn't
       work, the build will fail."""

class UpdateArg(FlagArgBase):
    """this option is the same as '-i --noclean'. It will update a single
        package that is already installed."""

class CleanupArg(FlagArgBase):
    """Clean your portage directory, to prevent emerge errors, removes
       empty directories and *.pyc files"""

class NoCopyArg(ObsoleteArgBase, FlagArgBase):
    """In older releases emerge would have
       copied everything from the SVN source tree to a source directory
       under %%KDEROOT%%\\tmp - currently nocopy is applied by default if
       EMERGE_NOCOPY is not set to "False". Be aware that setting
       EMERGE_NOCOPY to "False" might slow down the build process,
       irritate you and increase the disk space roughly by the size of
       SVN source tree."""

__init__()

# for debugging
if __name__ == "__main__":
    args = ArgBase.parser.parse_args()

    # put the values into their respective classes:
    for name in args.__dict__:
        value = args.__dict__[name]
        ArgBase.classByName[name].argValue = value
        if not value == False:
            print name, args.__dict__[name]
    givenCommands = list(x for x in ArgBase.classByName.values()
            if isinstance(x, CommandArgBase) and x.argValue)

    # now augment command list for meta commands like --full-package
    # or when no command is excplicitly given
    if not givenCommands:
        givenCommands = ArgBase.classByType([AllArg])
        # this cannot yet happen

    if args.__dict__['continue']: # continue is a reserved word
        commands = list(ArgBase.classByType[x] for x in ArgBase.classByType[AllArg].expand())
        if givenCommands[0] not in commands:
            print '--continue cannot be used with %s' % givenCommands[0].argStrings()[0]
            sys.exit(2)
        commands = commands[commands.index(givenCommands[0]):]
    else:
        if len(givenCommands) == 1:
            commands = (ArgBase.classByType[x] for x in givenCommands[0].expand())
        else:
            print 'at most one command may be given for a TARGET'
            sys.exit(2)

    # and execute all commands
    for command in commands:
        command.argValue = givenCommands[0].argValue
        print str(command)
        exitCode = command.execArg()
        # for success, commands do not need to return anything
        # for failure, they may return False or a numeric exit code
        if exitCode is None:
            exitCode = 0
        elif exitCode is False: # general case
            exitCode = 1
        if exitCode:
            sys.exit(exitCode)
