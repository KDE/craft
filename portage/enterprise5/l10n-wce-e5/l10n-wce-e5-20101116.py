import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4/%s'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
    

from Package.CMakePackageBase import *

class Package(PackageBase, SvnSource, CMakeBuildSystem, KDEWinPackager):
    def __init__( self  ):
        self.subinfo = subinfo()
        PackageBase.__init__( self )
        SvnSource.__init__( self )
        CMakeBuildSystem.__init__( self )
        KDEWinPackager.__init__( self )
        self.language = 'de'
        # because of the large amount of packages
        # it is very annoying to restart the build, 
        # wasting several hours, so ignore any errors 
        # for now
        self.subinfo.options.make.ignoreErrors = True
        self.subinfo.options.exitOnErrors = False
        # hardcoded for now
        #self.subinfo.options.package.version = '4.3.63'

    def repositoryUrl(self,index=0):
        # \todo we cannot use CMakePackageBase here because repositoryPath 
        # then is not be overrideable for unknown reasons 
        url = SvnSource.repositoryUrl(self,index) % self.language
        return url

    def checkoutDir(self,index=0):
        dir = SvnSource.checkoutDir(self,index) % self.language
        return dir
        
    def buildRoot(self):
        dir = os.path.join(PackageBase.buildRoot(self), self.language)
        return dir

    def qmerge(self):
        ''' When crosscompiling install l10n files
            also into the targets directory '''
        ret = PackageBase.qmerge(self)
        if emergePlatform.isCrossCompilingEnabled():
            utils.copyDir(self.imageDir(),
                    os.path.join(self.rootdir,
                    os.environ["EMERGE_TARGET_PLATFORM"]))
        return ret

    def unpack(self):
        autogen = os.path.join( self.packageDir() , "autogen.py" )
        if not SvnSource.unpack(self):
            return False
        # execute autogen.py and generate the CMakeLists.txt files
        # Possible autogen options are --disable-messages,
        # --disable-docs, --disable-data and --disable-scripts
        cmd = [ "python", autogen, self.language ]
        if emergePlatform.isCrossCompilingEnabled():
            cmd.append( "--disable-docs" )
        return self.system( cmd, cwd=os.path.join( self.sourceDir(), ".." ) )

    def configure(self):
        if not os.path.exists(os.path.join(self.buildDir(),"CMakeCache.txt")):
            return CMakeBuildSystem.configure(self)
        return True
        
    def createPackage(self):
        self.subinfo.options.package.packageName = 'l10n-kde4-%s' % self.language
        self.subinfo.options.package.withCompiler = False
        return KDEWinPackager.createPackage(self)
        
        
class MainInfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4/scripts'
        self.defaultTarget = 'svnHEAD'
        # all targets in svn
        self.languages  = 'af ar be bg bn bn_IN br ca cs csb cy da de '
        self.languages += 'el en_GB eo es et eu fa fi fr fy ga gl gu '
        self.languages += 'ha he hi hr hsb hu hy is it ja ka kk km kn ko ku '
        self.languages += 'lb lt lv mk ml ms mt nb nds ne nl nn nso oc '
        self.languages += 'pa pl pt pt_BR ro ru rw se sk sl sr sv '
        self.languages += 'ta te tg th tr uk uz vi wa xh zh_CN zh_HK zh_TW '

        #for testing
        self.languages  = 'de'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class MainPackage(PackageBase):
    def __init__( self  ):
        self.subinfo = MainInfo()
        PackageBase.__init__( self )
        self.kde4_l10n = portage.getPackageInstance('enterprise5','l10n-wce-e5')
        # set to any language to start building from 
        ## \todo when emerge.py is able to provide command line options to us
        # it would be possible to set this from command line 
        self.startLanguage = None 
        
    def execute(self):
        (command, option) = self.getAction()
        if self.isTargetBuild(): return True
        self.errors = dict()
        ## \todo does not work yet see note in PackageBase::getAction()
        if option <> None:
            languages = option.split()
        else:
            languages = self.subinfo.languages.split()
        found=None
            
        for language in languages:
            if not found and self.startLanguage:
                if self.startLanguage <> language:
                    continue
                else:
                    found = True
            
            self.kde4_l10n.language = language
            if not self.kde4_l10n.runAction(command):
                self.errors["%s-%s" % (language, command)] = 1

        print self.errors
        return True    
        
if __name__ == '__main__':
    MainPackage().execute()

