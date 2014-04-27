# -*- coding: utf-8 -*-
# kdepim-e5-package.py :
# This package will create a NSIS Installer that can be used to install
# a standalone Version of the KDE-Windows Platform necessary to use Kontact
# and other KDEPIM applications.

__author__  = "Andre Heinecke <aheinecke@intevation.de>"
__license__ = "GNU General Public License (GPL)"

import time

import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['en_de'] = ""
        # Target with german and english localization
        self.defaultTarget = 'en_de'

    def setDependencies( self ):
        self.dependencies[ 'libs/runtime' ] = 'default'
        self.dependencies[ 'kde/kdepim-runtime' ] = 'default'
        self.dependencies[ 'kde/kdepim' ] = 'default'
        self.dependencies[ 'kde/kde-l10n-de' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        # TODO: Split up the blacklist into smaller packages
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]

        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        # Basic nsis defines
        self.defines[ "executable" ] = "bin\\kontact.exe"
        self.defines[ "company" ] = os.getenv("EMERGE_COMPANY_NAME") or "KDE"
        self.defines[ "productname" ] = os.getenv("EMERGE_PRODUCT_NAME") or \
                                        "Kontact Enterprise 5"
        self.defines[ "setupname" ] = os.getenv("EMERGE_SETUP_NAME") or \
                                       "Kontact-E5"
        self.defines[ "setupname" ] = self.defines[ "setupname" ]+ "-%s.exe" % \
                                       time.strftime("%Y-%m-%d-%H-%M")
        self.defines[ "license" ] = os.getenv("EMERGE_LICENSE_FILE") or \
                self.imageDir() + "\\share\\apps\\LICENSES\\GPL_V2"
        self.scriptname = os.path.join( self.packageDir(),
                                        "kontact-e5-installer.nsi" )
        # Custom definitions
        self.defines[ "copyright" ] = os.getenv("EMERGE_COPYRIGHT") or \
             "Copyright (c) 2001-%s Kontact Authors" % \
                time.strftime("%Y")
        self.defines[ "productname_short" ] = os.getenv("EMERGE_PRODUCT_SHORTNAME") or \
                                              "Kontact E5"
        self.defines[ "description" ] = os.getenv("EMERGE_DESCRIPTION") or \
                                        "Kontact Enterprise 5 (beta)"
        # Version Number needs to be in the format x.x.x.x
        self.defines[ "version_number" ] = "4.6.0.0"
        self.defines[ "version_date" ] = time.strftime("%Y-%m-%d-%H-%M")
        self.defines[ "branding" ] = os.getenv("EMERGE_KDEPIME5_BRANDING") or \
                                     "includes\\branding.nsi"
        self.defines[ "branding_locale" ] = os.getenv("EMERGE_BRANDING_LOCALE") or \
                                     "includes\\branding-locale.nsi"



