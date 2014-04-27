# -*- coding: utf-8 -*-
# kdepim-e5-msi-package.py :
# This package will create a msi Installer Package that can be used to install
# a standalone Version of the KDE-Windows Platform necessary to use Kontact
# and other KDEPIM applications.

__author__  = "Andre Heinecke <aheinecke@intevation.de>, Patrick Spendrin <ps_ml@gmx.de>"
__license__ = "GNU General Public License (GPL)"

# to get this working, install http://wix.codeplex.com/releases/view/60102#DownloadId=204417
# and put it into the path

import time

import info
from Package.VirtualPackageBase import *
from Packager.MSInstallerPackager import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['en_de'] = ""
        # Target with german and english localization
        self.defaultTarget = 'en_de'

    def setDependencies( self ):
        self.dependencies[ 'libs/runtime' ] = 'default'
        self.dependencies[ 'enterprise5/kdepim-runtime-e5' ] = 'default'
        self.dependencies[ 'enterprise5/kdepim-e5' ] = 'default'
        self.dependencies[ 'binary/virtuoso' ] = 'default'
        self.dependencies[ 'enterprise5/l10n-wce-e5' ] = 'default'


class Package( MSInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        # TODO: Split up the blacklist into smaller packages
        blacklists = [ PackagerLists.runtimeBlacklist, 'blacklist.txt' ]

        MSInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        # Basic nsis defines
#        self.defines[ "executable" ] = "bin\\kontact.exe"
        self.defines[ "company" ] = os.getenv("EMERGE_COMPANY_NAME") or "KDE"
        self.defines[ "productname" ] = os.getenv("EMERGE_PRODUCT_NAME") or \
                                        "Kontact Enterprise 5"
#        self.defines[ "license" ] = os.getenv("EMERGE_LICENSE_FILE") or \
#                self.imageDir() + "\\share\\apps\\LICENSES\\GPL_V2"
        # Custom definitions
        self.defines[ "copyright" ] = os.getenv("EMERGE_COPYRIGHT") or \
             "Copyright (c) 2001-%s Kontact Authors" % \
                time.strftime("%Y")
#        self.defines[ "productname_short" ] = os.getenv("EMERGE_PRODUCT_SHORTNAME") or \
#                                              "Kontact E5"
        self.defines[ "description" ] = os.getenv("EMERGE_DESCRIPTION") or \
                                        "Kontact Enterprise 5 (beta)"
        # Version Number needs to be in the format x.x.x.x
#        self.defines[ "version_number" ] = "4.7.0.0"
#        self.defines[ "version_date" ] = time.strftime("%Y-%m-%d-%H-%M")
#        self.defines[ "branding" ] = os.getenv("EMERGE_KDEPIME5_BRANDING") or \
#                                     "includes\\branding.nsi"
#        self.defines[ "branding_locale" ] = os.getenv("EMERGE_BRANDING_LOCALE") or \
#                                     "includes\\branding-locale.nsi"



if __name__ == '__main__':
    Package().execute()
