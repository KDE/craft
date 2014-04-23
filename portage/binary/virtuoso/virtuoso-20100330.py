from Package.CMakePackageBase import *
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        if compiler.isX64():
            self.targets[ '20100330' ] =  'http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.1/vos6-win64-20100330.zip'
            self.targets['6.1.6'] = \
                "http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.6/virtuoso-opensource-win64-20120802.zip"
            self.targets['6.1.7'] = \
                "http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.7/virtuoso-opensource-x64-20130722.zip"
            self.targetDigests['20100330'] = '4b2d54eaa96f354d117b150a02b973f9cb54126e'
            self.targetDigests['6.1.6'] = '01385100ccada82873173d8f3180af94a8fb2a2a'
            self.targetDigests['6.1.7'] = '5921810147531c2cec8113325eb6d021f70fca3a'
        else:
            self.targets[ '20100330' ] = \
                'http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.1/vos6-win32-20100330.zip'
            self.targets['6.1.6'] = \
                "http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.6/virtuoso-opensource-win32-20120802.zip"
            self.targets['6.1.7'] = \
                "http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.7/virtuoso-opensource-x86-20130722.zip"
            self.targetDigests['20100330'] = 'f93f7606a636beefa4c669e8fc5d0100217d85c4'
            self.targetDigests['6.1.6'] = '7542bf14ec40517813a0d293c9e9023b1b305e62'
            self.targetDigests['6.1.7'] = 'c992abaa0708e95e45c5fd007d514ae6bc037a4e'
        for ver in [ '20100330', '6.1.6', '6.1.7' ]:
            self.targetInstSrc[ver] = "virtuoso-opensource"

        self.shortDescription = "a middleware and database engine hybrid for RDBMS, ORDBMS, virtual database, RDF, XML, free-text, web application server and file server functionality"
        self.defaultTarget = '6.1.7'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

class Package(CMakePackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None
    CMakePackageBase.__init__( self )


  def compile( self ):
    return True

  def install( self ):
    if( not self.cleanImage()):
      return False

    shutil.copytree( self.sourceDir() , self.installDir(),ignore=shutil.ignore_patterns('libexpat.dll' ))

    return True

if __name__ == '__main__':
    Package().execute()
