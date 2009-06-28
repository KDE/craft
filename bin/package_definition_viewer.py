# -*- coding: iso-8859-15 -*-
from xml.dom.minidom import *
import re
import os, sys

TAGDOKU = dict()
TAGDOKU['headline'] = """
The tags for kdewin-packager's xml files are the following:
"""

TAGDOKU['module']   = """
the root element.  It can have an attribute 'name' which contains the 
name of the package and thus defines the name of the 'default' package.
There has to be one xml file per KDE-module.
"""

TAGDOKU['package']  = """
defines a single package, which can have multiple package components
(called parts). The name of the package is determined by the (required)
attribute 'name'. There can be multiple 'package' tags per 'module'.
"""

TAGDOKU['part']  =  """
defines a package component (called parts). The known package components
are "runtime", "development", "documentation", "source" and "debug" 
The generated archive files contains related terms (bin, lib, doc, src, debug)
in the filename. There can be multiple 'part' tags per 'package'.
"""
TAGDOKU['files'] = """
Is a child tag of 'part' which describes a set of files for this package
component. There are attributes available for this tag: 

	include="<regexp>" 
		contains a specification of a perl compatible 
		regular expression for the files that should be 
		contained in the package. The tag content should 
		be empty in this case, which means the tag could 
		also be defined as <files include=".*"/>
		
When not using any attribute one can add relative file pathes 
separated by ';' or '\n' into the content of this tag. 
It is possible to have multiple 'files' tags per 'part' tag. They
will be executed subsequently.
"""

TAGDOKU['ignore']   = """
Is a child tag of 'package' which contains a perl compatible regular
expression for the files that should not be contained in any package.
It is possible to have multiple 'ignore' tags per 'package' tag. They
will be executed subsequently. 'ignore' tags will always precede
regexp' tags."""

TAGDOKU['shortDescription'] = """
Is a child tag of 'package' and contains the shortDescription used
in the Installer. NOTE: there is no other description yet.
"""

TAGDOKU['dependency'] = """
Is a child tag of 'package' and contains a package dependency of this 
package. It is possible to have multiple 'dependency' tags per 'package' 
tag.
"""
class Part:
    def __init__( self, name='' ):
        self.name = name
        self.reList = []
        self.filesList = []
        self.ignoreList = []
        self.ignoreFileList = []
        self.fileList = []

    def printFileList( self ):
        for fileName in self.fileList:
            print fileName

    def addFiles( self, include ):
        if include is None:
            return
        for file in include.split('\n'):
            self.filesList.append(file)

    def addInclude( self, include ):
        self.reList.append( re.compile( include ) )

    def addIgnore( self, regexp ):
        self.ignoreList.append( re.compile( regexp ) )

class SinglePackage:
    def __init__( self, name='' ):
        self.description = ''
        self.shortDescription = ''
        self.name = name
        self.isEmpty = False
        self.partList = list()

    def __repr__( self ):
        return self.name + ' - ' + self.shortDescription

        
class XmlPackager:
    packageList = list()
    fileList = []
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
            for i in range( len( element.getElementsByTagName( 'ignore' ) ) ):
                package.addIgnore( self._checkTag( element.getElementsByTagName( 'ignore' )[i] ) )
            for part in element.getElementsByTagName( 'part' ):
                package.partList.append(self._checkTag(part))
            self.packageList.append( package )            

    def handle_partTag( self, element ):
        if element.hasAttribute( 'name' ):
            part = Part(element.getAttribute( 'name' ))
            for i in range( len( element.getElementsByTagName( 'files' ) ) ):
                elem = element.getElementsByTagName( 'files' )[i]
                if elem.hasAttribute( 'include' ):
                    part.addInclude(elem.getAttribute( 'include' ))
                if len( elem.childNodes ) > 0:
                    part.addFiles(elem.childNodes[0].nodeValue)
        return part

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

    def handle_ignoreTag( self, element ):
        if len( element.childNodes ) > 0:
            return element.childNodes[0].nodeValue
        else:
            return None

    def split( self ):
        for root, dirs, files in os.walk( self.imagepath ):
            shortRoot = root.replace( self.imagepath + os.sep, '' )
            for fileName in files:
                name = os.path.join( shortRoot, fileName )
                name = name.replace( os.sep, '/' )
                self.fileList.append( name )

        for package in self.packageList:
            for part in package.partList:
                for reg in part.ignoreList:
                    for line in self.fileList:
                        regObj = reg.match( line )
                        if regObj:
                            part.ignoreFileList.append( line )
                    for z in part.ignoreFileList:
                        if z in self.fileList:
                            self.fileList.remove( z )

                for reg in part.reList:
                    for line in self.fileList:
                        regObj = reg.match( line )
                        if regObj:
                            part.fileList.append( line )
                    for z in part.fileList:
                        if z in self.fileList:
                            self.fileList.remove( z )

                for file in part.filesList:
                    for line in self.fileList:
                        if line == file:
                            part.fileList.append( line )
                    for z in part.fileList:
                        if z in self.fileList:
                            self.fileList.remove( z )

    def printUnusedFiles( self ):
        if len(self.fileList) > 0:
            print "unused files"
            for name in self.fileList:
                print name 

    def printOverview( self ):
        for package in self.packageList:
            for part in package.partList:
                if len( part.ignoreFileList ) == 0:
                    print package.name + ' ' + part.name, '\tcontaining', len( part.fileList ), 'files'
                else:
                    print package.name + ' ' + part.name, '\tcontaining', len( part.fileList ), 'files, ignoring', len( package.ignoreFileList ), 'files'

    def printList( self, name="" ):
        for package in self.packageList:
            print "package  " + package.name
            if name == "" or package.name == name:
                for part in package.partList:
                    print "part " + part.name
                    for filename in part.fileList:
                        print filename
                    if len( part.ignoreFileList ) > 0:
                        print 'ATTENTION: Ignoring:'
                        for filename in part.ignoreFileList:
                            print filename

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
    i = 1
    _printUnused = False
    _printList = False
    if sys.argv[i] == "--unused":
        _printUnused = True
        i = i+1
    elif sys.argv[i] == "--list":
        _printList = True
        i = i+1
    image = os.path.abspath( sys.argv[i] )
    i = i+1
    filename = sys.argv[i]
    i = i+1
    #image = 'C:\\daten\\kde\msvc-root\\tmp\\kdegraphics-20080202\\image-msvc2008'
    #filename = 'C:\\daten\\kde\msvc-root\\emerge\\portage\\kde\\kdegraphics\\kdegraphics-package.xml'

    fileobj = open( filename )

    try:
        doc = parse( fileobj )
    except xml.parsers.expat.ExpatError:
        print 'FATAL ERROR: The xml file might not be wellformed. Please check!'
        exit(1)

    packager = XmlPackager( doc, image )
    packager.split()
    if _printUnused:
        packager.printUnusedFiles()
        exit(0)
        
    if _printList == 1:
        packager.printList()
        exit(0)
    
    if len( sys.argv ) == 3:
        packager.printOverview()

    if len( sys.argv ) > 4 and sys.argv[3] == 'print':
        packager.printList( sys.argv[4] )
else:
    usage()
