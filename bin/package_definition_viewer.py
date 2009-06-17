# -*- coding: iso-8859-15 -*-
from xml.dom.minidom import *
import re
import os, sys

TAGDOKU = dict()
TAGDOKU['headline'] = """The tags for kdewin-packager's xml files are the following:"""
TAGDOKU['module']   = """the root element.  It can have an attribute 'name' which contains the """ \
                    + """name of the package and thus defines the name of the 'default' package. """ \
                    + """There has to be one xml file per KDE-module."""
TAGDOKU['package']  = """defines a single package, which can result in multiple packages (bin, """ \
                    + """lib, doc, src, debug, ...) with the name given by the (required) """ \
                    + """attribute 'name'. The package with the special name 'default' will be """ \
                    + """used to dump the remaining files. It will result in an error, if the """ \
                    + """attribute 'empty' has been set to 'true', for all other package names """ \
                    + """the result of the attribute 'empty' is undefined. There can be """ \
                    + """multiple 'package' tags per 'module'."""
TAGDOKU['regexp']   = """Is a child tag of 'package' which contains a perl compatible regular """ \
                    + """expression for the files that should be contained in the package. """ \
                    + """It is possible to have multiple 'regexp' tags per 'package' tag. They """ \
                    + """will be executed subsequently."""
TAGDOKU['ignore']   = """Is a child tag of 'package' which contains a perl compatible regular """ \
                    + """expression for the files that should not be contained in any package. """ \
                    + """It is possible to have multiple 'ignore' tags per 'package' tag. They """ \
                    + """will be executed subsequently. 'ignore' tags will always precede """ \
                    + """'regexp' tags."""
TAGDOKU['shortDescription'] = """Is a child tag of 'package' and contains the shortDescription used """\
                            + """in the Installer. NOTE: there is no other description yet."""

class SinglePackage:
    def __init__( self, name='' ):
        self.description = ''
        self.shortDescription = ''
        self.name = name
        self.fileList = []
        self.reList = []
        self.ignoreList = []
        self.ignoreFileList = []
        self.isEmpty = False

    def printFileList( self ):
        for fileName in self.fileList:
            print fileName

    def addRegExp( self, regexp ):
        self.reList.append( re.compile( regexp ) )

    def addIgnore( self, regexp ):
        self.ignoreList.append( re.compile( regexp ) )

    def __repr__( self ):
        return self.name + ' - ' + self.shortDescription
        
class XmlPackager:
    packageList = list()
    def __init__( self, document, imagepath ):
        self.imagepath = imagepath
        self._checkTag( document.getElementsByTagName( 'module' )[0] )

    def _checkTag( self, element ):
        functionName = 'handle_' + element.tagName + 'Tag'

        if hasattr( self, functionName ):
            func = getattr( self, functionName )
            return func( element )

    def handle_moduleTag( self, element ):
        for package in element.getElementsByTagName( 'package' ):
            self._checkTag( package )

    def handle_packageTag( self, element ):
        if element.hasAttribute( 'name' ):
            package = SinglePackage( element.getAttribute( 'name' ) )
            if element.getAttribute( 'name' ) == 'default':
                if element.hasAttribute( 'empty' ) and element.getAttribute( 'empty' ) == 'true':
                    package.isEmpty = True
            if len( element.getElementsByTagName( 'description' ) ) > 0:
                package.description = self._checkTag( element.getElementsByTagName( 'description' )[0] )
            if len( element.getElementsByTagName( 'shortDescription' ) ) > 0:
                package.shortDescription = self._checkTag( element.getElementsByTagName( 'shortDescription' )[0] )
            for i in range( len( element.getElementsByTagName( 'regexp' ) ) ):
                package.addRegExp( self._checkTag( element.getElementsByTagName( 'regexp' )[i] ) )
            for i in range( len( element.getElementsByTagName( 'ignore' ) ) ):
                package.addIgnore( self._checkTag( element.getElementsByTagName( 'ignore' )[i] ) )
            self.packageList.append( package )            

    def handle_descriptionTag( self, element ):
        if len( element.childNodes ) > 0:
            return element.childNodes[0].nodeValue
        else:
            return None

    def handle_shortDescriptionTag( self, element ):
        if len( element.childNodes ) > 0:
            return element.childNodes[0].nodeValue
        else:
            return None

    def handle_regexpTag( self, element ):
        if len( element.childNodes ) > 0:
            return element.childNodes[0].nodeValue
        else:
            return None

    def handle_ignoreTag( self, element ):
        if len( element.childNodes ) > 0:
            return element.childNodes[0].nodeValue
        else:
            return None

    def split( self ):
        fileList = []
        for root, dirs, files in os.walk( self.imagepath ):
            shortRoot = root.replace( self.imagepath + os.sep, '' )
            for fileName in files:
                name = os.path.join( shortRoot, fileName )
                name = name.replace( os.sep, '/' )
                fileList.append( name )

        defaultPackage = None
        for package in self.packageList:
            for reg in package.ignoreList:
                for line in fileList:
                    regObj = reg.match( line )
                    if regObj:
                        package.ignoreFileList.append( line )
                for z in package.ignoreFileList:
                    if z in fileList:
                        fileList.remove( z )

            if package.name == 'default':
                defaultPackage = package
                continue

            for reg in package.reList:
                for line in fileList:
                    regObj = reg.match( line )
                    if regObj:
                        package.fileList.append( line )
                for z in package.fileList:
                    if z in fileList:
                        fileList.remove( z )

        if len(fileList) > 0:
            if defaultPackage:
                if defaultPackage.isEmpty:
                    print "ERROR: The default package is supposed to be empty but there are files left over!"
                for name in fileList:
                    defaultPackage.fileList.append( name )
            else:
                print "ERROR: No default package is available but there are one or more files left over!"
                exit(1)
                        

    def printOverview( self ):
        for package in self.packageList:
            if len( package.ignoreFileList ) == 0:
                print package, '\tcontaining', len( package.fileList ), 'files'
            else:
                print package, '\tcontaining', len( package.fileList ), 'files, ignoring', len( package.ignoreFileList ), 'files'

    def printList( self, name ):
        for package in self.packageList:
            if package.name == name:
                for filename in package.fileList:
                    print filename
                if len( package.ignoreFileList ) > 0:
                    print 'ATTENTION: Ignoring:'
                    for filename in package.ignoreFileList:
                        print filename

                return
        print 'ERROR: No suitable package was found!'
        exit(1)

def usage():
    print 'Syntax:'
    print os.path.basename( sys.argv[0] ) + ' imagepath X:\\kde\\package.xml command [options]'
    print
    print 'imagepath  \t\tthe directory containing the files which have'
    print '           \t\tto be packaged'
    print 'X:\\kde\\package.xml\tthe path to the xml file containing the'
    print '           \t\tdefinition for the subpackages'
    print
    print 'command is one of the following:'
    print 'print [packageName]  \tprint all files within packageName'
    print
    print 'without command the overview over all packages is printed'
    print
    print '-'*79
    print
    keys = TAGDOKU.keys()
    keys.sort()
    print TAGDOKU['headline']
    keys.remove('headline')
    for tag in keys:
        print '- ' + tag
        print TAGDOKU[tag]
        print

if len( sys.argv ) > 2:
    image = os.path.abspath( sys.argv[1] )
    filename = sys.argv[2]
    #image = 'C:\\kde\\kde-msvc\\tmp\\kdegraphics-20080202\\image-msvc2008'
    #filename = 'C:\\kde\\kde-msvc\\emerge\\portage\\kde\\kdegraphics\\kdegraphics-package.xml'

    fileobj = open( filename )

    try:
        doc = parse( fileobj )
    except xml.parsers.expat.ExpatError:
        print 'FATAL ERROR: The xml file might not be wellformed. Please check!'
        exit(1)

    packager = XmlPackager( doc, image )
    packager.split()

    if len( sys.argv ) == 3:
        packager.printOverview()

    if len( sys.argv ) > 4 and sys.argv[3] == 'print':
        packager.printList( sys.argv[4] )
else:
    usage()
