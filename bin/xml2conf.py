# translate xml package split description file to kdewin-installer config file
import sys
import re

compilerList = ( "x86-mingw4", "x64-mingw4", "vc100" )

moduleStart = re.compile( r"<module name=\"([^\"]*)\">" )
packageStart = re.compile( r"<package name=\"([^\"]*)\"[ ]?(?:comment=.*(meta).*)?>" )
packageEnd = re.compile( r"</package>" )
dependencyTerm = re.compile( r"<dependency>([^<]*)</dependency>" )
descriptionTerm = re.compile( r"<shortDescription>([^<]*)</shortDescription>" )

class Xml2Conf:
    def __init__( self ):
        self.packageDepsList = dict()
        self.packageDescriptionList = dict()
        self.moduleMetaName = ""
        self.moduleName = ""

    def parseFile( self, filename ):
        with open( filename ) as infile:
            for line in infile:
                result = moduleStart.search( line )
                if result:
                    self.moduleName = result.group( 1 )
                    for sline in infile:
                        result = packageStart.search( sline )
                        if result:
                            packageName = result.group( 1 )
                            if result.group( 2 ) == "meta":
                                self.moduleMetaName = packageName
                            self.packageDepsList[ packageName ] = []
                            for subline in infile:
                                result = dependencyTerm.search( subline )
                                if result:
                                    self.packageDepsList[ packageName ].append( result.group( 1 ) )
                                result = descriptionTerm.search( subline )
                                if result and not packageName == self.moduleMetaName:
                                    self.packageDescriptionList[ packageName ] = result.group( 1 )
                                if packageEnd.search( subline ):
                                    break


    def getMetaPackageString( self ):
        ret = ""
        # print the metapackage line
        if self.moduleMetaName:
            print "@metapackage", self.moduleMetaName,
            for i in self.packageDepsList[ self.moduleMetaName ]:
                print i,
            print
            self.packageDepsList.pop( self.moduleMetaName, "" )
        print ';'
    
    def __str__( self ):
        moduleList = dict()
        retString = str( self.packageDepsList )
        retString += str( self.packageDescriptionList )
        
        # print the header
#        print ';'+"-"*55
#        print ';', moduleName
#        print ';'+"-"*55


        # print the categorypackages
        for compiler in compilerList:
#            print "@categorypackages KDE",
            for package in self.packageDepsList:
#                print package + "-" + compiler,
                pass
#            print
#        print ';'

        # print all dependencies
        for compiler in compilerList:
            for package in self.packageDepsList:
#                print "@deps", package + "-" + compiler,
                for i in self.packageDepsList[ package ]:
#                    print i + "-" + compiler,
                    pass
#                print
#        print ';'

        moduleList[ self.moduleName ] = self.packageDescriptionList

#        print
#        print ';' + '-' * 55
#        print
        for module in moduleList:
            for package in moduleList[ module ]:
#                print "@pkgnotes", package + "-*", moduleList[ module ][ package ]
                pass
#            print
        return retString

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print "not enough arguments"
        sys.exit( 0 )

    x = Xml2Conf()

    for filename in sys.argv[ 1: ]:
        x.parseFile( filename )
    print x