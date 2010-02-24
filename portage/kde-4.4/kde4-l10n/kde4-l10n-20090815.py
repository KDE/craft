import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4/%s'
        self.defaultTarget = 'svnHEAD'
        self.svnTargets['svnHEAD'] = 'branches/stable/l10n-kde4/%s'
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.4.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.4.' + ver + '/src/kde-l10n/kde-l10n-%s-4.4.' + ver + '.tar.bz2'
          self.targetInstSrc['4.4.' + ver] = 'kde-l10n-%s-4.4.' + ver
        self.defaultTarget = 'svnHEAD'
        
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
#        self.hardDependencies['kde-4.4/kdelibs'] = 'default'
    

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self  ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.language = None
        # because of the large amount of packages
        # it is very annoying to restart the build, 
        # wasting several hours, so ignore any errors 
        # for now
        self.subinfo.options.make.ignoreErrors = True
        self.subinfo.options.exitOnErrors = False
        # hardcoded for now
        #self.subinfo.options.package.version = '4.4.63'
        # overwrite the workDir function that is inherited from SourceBase
        self.source.workDir = self.workDir.__get__(self, Package)
        self.source.localFileNames = self.localFileNames.__get__(self, Package)

    def localFileNames(self):
        filenames = []
        for i in range( self.repositoryPathCount() ):
            filenames.append( os.path.basename( self.repositoryPath( i ) ) )
            print i
        return filenames

    def configureSourceDir(self):
        return CMakePackageBase.configureSourceDir( self ) % self.language

    def repositoryPath(self,index=0):
        # \todo we cannot use CMakePackageBase here because repositoryPath 
        # then is not be overrideable for unknown reasons 
        url = CMakePackageBase.repositoryPath(self,index) % self.language
        return url

    def workDir(self):
        dir = os.path.join(CMakePackageBase.workDir(self), self.language)
        return dir

    def fetch(self):
        filenames = self.localFileNames()

        if ( self.source.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True

        self.source.setProxy()
        if self.subinfo.hasTarget():
            return utils.getFiles( self.subinfo.target() % self.language, self.downloadDir() )
        else:
            return utils.getFiles( "", self.downloadDir() )

    def unpack(self):
        autogen = os.path.join( self.packageDir() , "autogen.py" )

        filenames = self.localFileNames()

        # the following code is taken from ArchiveSource::unpack() function
        # it will not remove already existing files
        destdir = self.workDir()
        utils.debug( "unpacking files into work root %s" % destdir, 1 )

        for filename in filenames:
            utils.debug( "unpacking this file: %s" % filename, 1 )
            if ( not utils.unpackFile( self.downloadDir(), filename, destdir ) ):
                return False

        # execute autogen.py and generate the CMakeLists.txt files
        cmd = "cd %s && python %s %s %s" % \
              ('..', autogen, self.sourceDir() % self.language, self.language )
        return self.system( cmd )

    def configure(self):
        if not os.path.exists(os.path.join(self.buildDir(),"CMakeCache.txt")):
            return CMakePackageBase.configure(self)
        return True
        
    def createPackage(self):
        self.subinfo.options.package.packageName = 'kde4-l10n-%s' % self.language
        self.subinfo.options.package.withCompiler = False
        return CMakePackageBase.createPackage(self)
        
        
class MainInfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4/scripts'
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.4.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.4.' + ver + '/src/kde-l10n/kde4-l10n-' + 'de' + '-4.4.' + ver + '.tar.bz2' 
        self.defaultTarget = 'svnHEAD'
        # all targets in svn
        self.languages  = 'af ar be bg bn bn_IN br ca cs csb cy da de '
        self.languages += 'el en_GB eo es et eu fa fi fr fy ga gl gu '
        self.languages += 'ha he hi hr hsb hu hy is it ja ka kk km kn ko ku '
        self.languages += 'lb lt lv mk ml ms mt nb nds ne nl nn nso oc '
        self.languages += 'pa pl pt pt_BR ro ru rw se sk sl sr sv '
        self.languages += 'ta te tg th tr uk uz vi wa xh zh_CN zh_HK zh_TW '

        #for testing
        self.languages  = 'fr de'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
#        self.hardDependencies['kde-4.4/kdelibs'] = 'default'
    
    
class MainPackage(CMakePackageBase):
    def __init__( self  ):
        self.subinfo = MainInfo()
        CMakePackageBase.__init__( self )
        self.kde4_l10n = portage.getPackageInstance('kde-4.4','kde4-l10n')
        # set to any language to start building from 
        ## \todo when emerge.py is able to provide command line options to us
        # it would be possible to set this from command line 
        self.startLanguage = None 
        
    def execute(self):
        (command, option) = self.getAction()
        self.errors = dict()
        ## \todo does not work yet see note in PackageBase::getAction()
#        if option <> None:
#            languages = option.split()
#        else:
        languages = self.subinfo.languages.split()
        found=None
        for language in languages:
            if not found and self.startLanguage:
                if self.startLanguage <> language:
                    continue
                else:
                    found = True
            
            self.kde4_l10n.language = language
            utils.debug("current language: %s" % self.kde4_l10n.language, 1)
            self.kde4_l10n.runAction(command)
#                self.errors["%s-%s" % (language, command)] = 1

        utils.debug("Errors that happened while executing last command: %s" % self.errors, 2)
        return True    
        
if __name__ == '__main__':
    MainPackage().execute()

