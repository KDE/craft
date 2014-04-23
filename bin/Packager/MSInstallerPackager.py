# copyright (c) 2011 Patrick Spendrin <ps_ml@gmx.de>

import uuid
from xml.dom.minidom import Document
import hashlib
from string import Template
from io import StringIO
import re

from .CollectionPackagerBase import *


class MSInstallerPackager( CollectionPackagerBase ):
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__( self, whitelists, blacklists )

    uniqueFileIds = dict()
    __beginString = re.compile( r"(^[^A-Za-z_])" )
    __invalidChars = re.compile( r"[^A-Za-z0-9_.]" )

    def __getUniqueIdString( self, fileName ):
        fixedName = self.__invalidChars.sub( r"_", fileName )
        fixedName = self.__beginString.sub( r"_\1", fixedName )

        if fixedName in self.uniqueFileIds:
            self.uniqueFileIds[ fixedName ] += 1
            return fixedName + "_" + str( self.uniqueFileIds[ fixedName ] )
        else:
            self.uniqueFileIds[ fixedName ] = 1
            return fixedName


    def generateMSInstaller( self ):
        """ runs tools to generate the installer itself """
        if self.package.endswith( "-package" ):
            shortPackage = self.package[ : -8 ]
        else:
            shortPackage = self.package
        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = "%s-setup-%s.msi" % ( shortPackage, self.buildTarget )
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.imageDir()
        if not "company" in self.defines or not self.defines[ "company" ]:
            self.defines[ "company" ] = "KDE"
        if not "productname" in self.defines or not self.defines[ "productname" ]:
            self.defines[ "productname" ] = "%s %s" % ( shortPackage.capitalize(), self.buildTarget )
        if not "executable" in self.defines or not self.defines[ "executable" ]:
            self.defines[ "executable" ] = ""
        if not "productuid" in self.defines or not self.defines[ "productuid" ]:
            m = hashlib.md5()
            m.update( self.defines[ "productname" ] )
            m.update( self.defines[ "setupname" ] )
            self.defines[ "productuid" ] = str( uuid.UUID( hex=m.hexdigest() ) )
            print(self.defines[ "productuid" ])
        if not "upgradeuid" in self.defines or not self.defines[ "upgradeuid" ]:
            self.defines[ "upgradeuid" ] = str( uuid.uuid4() )
        if not "componentuid" in self.defines or not self.defines[ "componentuid" ]:
            self.defines[ "componentuid" ] = str( uuid.uuid4() )
        if not self.scriptname:
            self.scriptname = os.path.join( os.path.dirname( __file__ ), "MSInstaller.wxs.template" )

        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

        utils.new_line()
        utils.debug( "generating installer %s" % self.defines[ "setupname" ] )

        wxs = Document()
        componentRefs = Document()

        rootObject = wxs.createElement( "Directory" )
        componentRoot = componentRefs.createElement( "Feature" )

        objectDict = dict()
        objectDict[ self.imageDir() ] = rootObject
        rootObject.setAttribute( "Id", self.__getUniqueIdString( self.defines[ "productname" ] ) )
        rootObject.setAttribute( "Name", self.defines[ "productname" ] )

        componentRoot.setAttribute( "Id", "DefaultFeature" )
        componentRoot.setAttribute( "Title", "default feature" )
        componentRoot.setAttribute( "Level", "1" )

        for root, dirs, files in os.walk(self.imageDir()):
            if root == self.imageDir(): continue
            if files or dirs:
                currentDirectory = wxs.createElement( "Directory" )
                currentDirectory.setAttribute( "Id", self.__getUniqueIdString( os.path.basename(root) ) )
                currentDirectory.setAttribute( "Name", os.path.basename(root) )

                objectDict[ os.path.dirname(root) ].appendChild( currentDirectory )
                objectDict[ root ] = currentDirectory

                # components could be used to create updateable packages according to current
                # emerge packaging
                for _f in files:
                    _fileId = self.__getUniqueIdString( _f )
                    currentComponent = wxs.createElement( "Component" )
                    currentComponent.setAttribute( "Id", _fileId )
                    currentComponent.setAttribute( "Guid", str( uuid.uuid4() ) )
                    currentDirectory.appendChild( currentComponent )

                    currentComponentRef = componentRefs.createElement( "ComponentRef" )
                    currentComponentRef.setAttribute( "Id", _fileId )
                    componentRoot.appendChild( currentComponentRef )

                    currentFile = wxs.createElement( "File" )
                    currentFile.setAttribute( "Id", _fileId )
                    currentFile.setAttribute( "Source", os.path.join( "SourceDir", os.path.relpath( root, self.imageDir() ), _f ) )
                    currentComponent.appendChild( currentFile )

        if self.scriptname.endswith( ".template" ): outName = os.path.join( self.buildDir(), os.path.basename( self.scriptname )[:-9] )
        else: outName = os.path.join( self.buildDir(), self.scriptname )
        out = open( outName, 'w' )

        filelistString = StringIO()
        componentlistString = StringIO()

        rootObject.writexml( filelistString, " "*16, "    ", "\n" )
        componentRoot.writexml( componentlistString, " "*8, "    ", "\n" )

        self.defines[ "filelist" ] = filelistString.getvalue()
        self.defines[ "componentlist" ] = componentlistString.getvalue()
        filelistString.close()
        componentlistString.close()

        templateFile = open( self.scriptname, 'r' )
        scriptTemplate = Template( templateFile.read() )

        substitutedScript = scriptTemplate.safe_substitute( self.defines )
        out.write( substitutedScript )
        out.close()

        utils.system( "candle -o %s.wixobj %s" % ( outName, outName ) )
        utils.system( "light -b %s -o %s %s.wixobj" % ( self.imageDir(), os.path.join( self.packageDir(), self.defines[ "setupname" ] ), outName ) )

    def createPackage( self ):
        """ create a package """
        print("packaging using the MSInstallerPackager")
        
        self.internalCreatePackage()

        self.generateMSInstaller()
        return True
