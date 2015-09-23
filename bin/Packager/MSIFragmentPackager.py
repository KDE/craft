#
# copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
#

import portage
from xml.dom.minidom import Document
import hashlib
import uuid
#import re

from Packager.PackagerBase import *

def getUniqueIdString( fileName, root ):
    m = hashlib.md5()
    m.update( os.path.join( root, fileName ).encode( "latin-1" ) )
    return "file_" + m.hexdigest()

def getUniqueDirectoryId( relDirName ):
    m = hashlib.md5()
    m.update( os.path.join( relDirName ).encode( "latin-1" ) )
    return "dir_" + m.hexdigest()

class MSIFragmentPackager( PackagerBase ):
    uniqueFileIds = dict()
    uniqueDirectoryRefs = dict()
    checkDirDict = dict()

    __beginString = re.compile( r"(^[^A-Za-z_])" )
    __invalidChars = re.compile( r"[^A-Za-z0-9_.]" )

    def __init__( self, initialized = False ):
        if not initialized: PackagerBase.__init__( self )
        utils.debug( "MSIFragmentPackager __init__", 2 )
        self.outfile = os.path.join( self.packageDestinationDir(), "%s.wxs" % self.package )
        self.objfile = self.outfile.replace( "wxs", "wix" ) + "obj"


    def generateFragment( self ):
        wxs = Document()
        wix = wxs.createElement( "Wix" )
        wix.setAttribute( "xmlns", "http://schemas.microsoft.com/wix/2006/wi" )
        wxs.appendChild( wix )
        fragmentElement = wxs.createElement( "Fragment" )
        componentGroup = wxs.createElement( "ComponentGroup" )
        componentGroup.setAttribute( "Id", "%sComponentGroup" % self.package.replace( '-', '_' ) )
        wix.appendChild( fragmentElement )
        fragmentElement.appendChild( componentGroup )

        for root, dirs, files in os.walk( self.imageDir() ):
            if root == self.imageDir(): continue

            relDir = os.path.relpath( root, self.imageDir() )
            dirId = getUniqueDirectoryId( relDir )

            # components could be used to create updateable packages according to current
            # emerge packaging
            for _f in files:
                if _f.endswith( ".pdb" ) or _f.endswith( ".ilk" ): continue

                _fileId = getUniqueIdString( _f, root )
                currentComponent = wxs.createElement( "Component" )
                currentComponent.setAttribute( "Id", _fileId )
                currentComponent.setAttribute( "Directory", dirId )
                currentComponent.setAttribute( "Guid", str( uuid.uuid4() ) )
                componentGroup.appendChild( currentComponent )

                currentFile = wxs.createElement( "File" )
                currentFile.setAttribute( "Id", _fileId )
                currentFile.setAttribute( "KeyPath", "yes" )
                currentFile.setAttribute( "Source", os.path.join( "$(var.%sImageDir)" % self.package, relDir, _f ) )
                currentComponent.appendChild( currentFile )

        #out = open( self.outfile, 'w' )
        #wxs.writexml( out, "", "    ", "\n", encoding = "utf-8" )
        #out.close()

        #utils.system( "candle -o %s -d%sImageDir=%s %s" % ( self.objfile, self.package, self.imageDir(), self.outfile ) )


    def createPackage( self ):
        result = True
        self.generateFragment()
        return result

    def make_package( self ):
        return self.createPackage()
