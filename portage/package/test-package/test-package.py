import info
import portage
from xml.dom.minidom import Document
import hashlib
from string import Template
from io import StringIO
import uuid
import re

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0.1']:
          self.svnTargets[ ver ] = ''

        self.defaultTarget = '0.1'


    def setDependencies( self ):
        #self.buildDependencies['dev-util/frameworks-sdk'] = 'default'
        #self.buildDependencies['dev-util/emerge'] = 'default'
        #self.dependencies['frameworks/attica'] = 'default'
        #self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/tier1'] = 'default'
        self.dependencies['frameworks/tier2'] = 'default'
        #self.dependencies['frameworks/tier3'] = 'default'
        #self.dependencies['frameworks/tier4'] = 'default'


from Package.VirtualPackageBase import *
from Packager.CollectionPackagerBase import *
from Packager.MSIFragmentPackager import getUniqueIdString, getUniqueDirectoryId

class Package( VirtualPackageBase, CollectionPackagerBase ):
    def __init__( self, **args ):
        VirtualPackageBase.__init__( self )
        CollectionPackagerBase.__init__( self )
        self.dirs = dict()

    def __getPackages( self ):
        """return package instances for all dependencies"""
        packages = []
        directDependencies = portage.getDependencies( self.category, self.package )

        depList = []
        for ( category, package, _, _ ) in directDependencies:
            # unlike in CollectionPackagerBase, we want all dependencies here
            portage.solveDependencies( category, package, depList = depList )
        depList.reverse()
        for x in depList:
            # Ignore dev-utils that are wrongly set as hard dependencies
            if x.category == "dev-util" or x.package in ['wget', 'patch', 'sed'] or portage.PortageInstance.isVirtualPackage( x.category, x.package ):
                continue
            _package = portage.getPackageInstance( x.category, x.package )

            packages.append( _package )
        return packages


    def getFeatureXML( self, wxs, package, description, hidden=False ):
        if not wxs.ownerDocument: doc = wxs
        else: doc = wxs.ownerDocument
        componentRoot = doc.createElement( "Feature" )

        componentRoot.setAttribute( "Id", "%sFeature" % package.replace( '-', '_' ) )
        componentRoot.setAttribute( "Title", "%s" % package )
        if description: componentRoot.setAttribute( "Description", description )
        componentRoot.setAttribute( "Level", "1" )
        if hidden: display = "hidden"
        else: display = "collapse"
        componentRoot.setAttribute( "Display", display )

        componentGroupRef = doc.createElement( "ComponentGroupRef" )
        componentGroupRef.setAttribute( "Id", "%sComponentGroup" % package.replace( '-', '_' ) )
        componentRoot.appendChild( componentGroupRef )

        wxs.appendChild(componentRoot)

    def generateDirectoryFragments( self ):
        wxs = Document()
        wix = wxs.createElement( "Wix" )
        wix.setAttribute( "xmlns", "http://schemas.microsoft.com/wix/2006/wi" )
        wxs.appendChild( wix )
        for _dirref in sorted( self.dirs.keys() ):
            fragment = wxs.createElement( "Fragment" )
            wix.appendChild( fragment )
            directoryRef = wxs.createElement( "DirectoryRef" )
            _dirrefId = getUniqueDirectoryId( _dirref )
            if _dirref  == ".":
                _dirrefId = "INSTALLDIR"
            directoryRef.setAttribute( "Id", _dirrefId )
            fragment.appendChild( directoryRef )
            for _dir in self.dirs[ _dirref ]:
                dirElement = wxs.createElement( "Directory" )
                if not _dirref == ".":
                    _id = getUniqueDirectoryId( os.path.join( _dirref, _dir ) )
                else:
                    _id = getUniqueDirectoryId( _dir )
                dirElement.setAttribute( "Id", _id )
                dirElement.setAttribute( "Name", _dir )
                directoryRef.appendChild( dirElement )

        outfile = os.path.join( self.imageDir(), "_directories.wxs" )
        out = open( outfile, 'w' )
        wxs.writexml( out, "", "    ", "\n", encoding = "utf-8" )
        out.close()

        objfile = outfile.replace( "wxs", "wix" ) + "obj"
        utils.system( "candle -o %s %s" % ( objfile, outfile ) )
        return objfile

    def createPackage( self ):
        # handle direct dependencies special
        deps = portage.getDependencies( self.category, self.package )
        frameworks = [ package for _, package, _, _ in deps ]

        qtFrameworks = []
        basePackages = []
        objectFiles = []

        dependenciesCode = ""
        qtFrameworksCode = ""
        kfFrameworksCode = ""

        # run heat on all image directories
        _packages = self.__getPackages()

        def generateFeature(base, id, title, description):
            if not base.ownerDocument: base.ownerDocument = base
            t = base.ownerDocument.createElement( "Feature" )
            t.setAttribute( "Id", id )
            t.setAttribute( "Title", title )
            t.setAttribute( "Description", description )
            t.setAttribute( "Level", "1" )
            return t

        binwxsdoc = Document()
        qt5wxsdoc = Document()
        kf5wxsdoc = Document()

        kf5wxs = generateFeature(kf5wxsdoc, 'KF5Frameworks', 'KF5 Frameworks', 'The KDE Frameworks')
        binwxs = generateFeature(binwxsdoc, 'Dependencies', 'the 3rdparty dependencies', 'the 3rdparty dependencies')
        binwxs.setAttribute("Display", "hidden")
        qt5wxs = generateFeature(qt5wxsdoc, 'Qt5Frameworks', 'Qt5 Frameworks', 'The KDE build of Qt5KF5Frameworks')
        tiers = dict()
        _descriptions = { 'tier1': 'Tier 1 - only Qt dependencies',
                          'tier2': 'Tier 2 - Qt and Tier 1 dependencies',
                          'tier3': 'Tier 3 - Qt, Tier 1 and Tier 2 dependencies',
                          'tier4': 'Tier 4 - Qt, Tier 1, Tier 2 and Tier 3 dependencies' }
        for i in range( 4 ):
            tiername = 'tier' + str( i + 1 )
            print( tiername )
            t = generateFeature( kf5wxs, tiername, "Tier " + str( i + 1 ), _descriptions[ tiername ] )
            print( t )
            kf5wxs.appendChild( t )
            tiers[ tiername ] = t

        for package in _packages:
            tiername, _ = portage.getSubPackage( package.category, package.package )
            if not (tiername and tiername.startswith("tier")) and package.category != "libs":
                basePackages.append( package.package )
                self.getFeatureXML( binwxs, package.package, package.subinfo.shortDescription, True )
            elif package.category == "libs":
                qtFrameworks.append( package.package )
                self.getFeatureXML( qt5wxs, package.package, package.subinfo.shortDescription )
            else:
                # assume this is a kf5 framework
                if tiername in tiers:
                    self.getFeatureXML( tiers[ tiername ], package.package, package.subinfo.shortDescription )
                else:
                    self.getFeatureXML( kf5wxs, package.package, package.subinfo.shortDescription )

            package.changePackager( "MSIFragmentPackager" )
            package.outDestination = self.imageDir()
            package.createPackage()
            for x in package.objectFiles:
                objectFiles.append( x )

            imgDir = package.imageDir()
            for root, dirs, _ in os.walk( imgDir ):
                relRoot = os.path.relpath( root, imgDir )
                if len( dirs ) > 0:
                    if relRoot in self.dirs:
                        for x in dirs: 
                            if x not in self.dirs[ relRoot ]: self.dirs[ relRoot ].append( x )
                    else:
                        self.dirs[ relRoot ] = dirs

        print( '=' * 20 )
        for p in basePackages: print( p )
        print( '-' * 20 )
        for p in qtFrameworks: print( p )
        print( '-' * 20 )
        for p in frameworks: print( p )
        print( '=' * 20 )

        # generate base file
        templateFile = open( os.path.join( self.packageDir(), "main.wxs.template" ), 'r' )
        scriptTemplate = Template( templateFile.read() )

        iconCode = """<Icon Id="Foobar10.exe" SourceFile="FoobarAppl10.exe" />"""
        iconCode = ""
        
        s = StringIO()
        qt5wxs.writexml(s, " " * 8, " " * 4, "\n")
        qtFrameworksCode = s.getvalue()
        s = StringIO()
        kf5wxs.writexml(s, " " * 8, " " * 4, "\n")
        kfFrameworksCode = s.getvalue()
        s = StringIO()
        binwxs.writexml(s, " " * 8, " " * 4, "\n")
        dependenciesCode = s.getvalue()

        substitutedScript = scriptTemplate.safe_substitute( { 'dependenciesCode': dependenciesCode, 'qtFrameworksCode': qtFrameworksCode, 'kfFrameworksCode': kfFrameworksCode, 'iconCode': iconCode } )

        outfile = os.path.join( self.imageDir(), "_main.wxs" )
        out = open( outfile, 'w' )
        out.write( substitutedScript )
        out.close()
        objfile = outfile.replace( "wxs", "wix" ) + "obj"
        utils.system( "candle -o %s %s" % ( objfile, outfile ) )
        objectFiles.append( objfile )

        objfile = self.generateDirectoryFragments()
        objectFiles.append( objfile )
        #objectFiles.append( os.path.join( self.imageDir(), "icon.wixobj" ) )

        outputName = os.path.join( self.packageDestinationDir(), "test-package.msi" )
        #print( objectFiles )
        linkCmd = "light -ext WixUIExtension -o %s %s" % ( outputName, " ".join( objectFiles ) )
        #print( linkCmd )
        utils.system( linkCmd )
        return True

    def package( self ):
        self.createPackage()
        return True

