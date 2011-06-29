import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:emerge'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['dev-util/doxygen'] = 'default'

from Package.CMakePackageBase import *
from Source.SvnSource import *
from BuildSystem.BuildSystemBase import *
from datetime import date

class Package(PackageBase,GitSource,BuildSystemBase):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        GitSource.__init__(self)
        BuildSystemBase.__init__(self,"")
        self.subinfo.options.merge.destinationPath = "dev-utils"

    def checkoutDir(self, index=0 ):
        return os.path.join(ROOTDIR,"emerge")
        
    def configure(self):
        doxygenSourcePathes = "%s %s" % (os.path.join(self.checkoutDir(),'bin'),os.path.join(self.checkoutDir(),'doc'))

        # copy and patch template
        sourceDoxyFile = os.path.join(self.checkoutDir(),'doc','Doxyfile')
        destPath = self.buildDir()
        destDoxyFile = os.path.join(destPath,'Doxyfile')

        if not os.path.exists(destPath):
            utils.createDir(destPath)

        fin = open (sourceDoxyFile, "r")
        fout = open (destDoxyFile, "w")
        for line in fin:
            if line.find("@INPUT@") <> -1:
                line = line.replace("@INPUT@",doxygenSourcePathes)
            elif line.find("@PROJECT_NUMBER@") <> -1:
                line = line.replace("@PROJECT_NUMBER@",date.today().isoformat())
            fout.write(line)
        fin.close()
        fout.close()
        return True

    def make(self):
        buildPath = self.buildDir()
        doxyFile = os.path.join(buildPath,'Doxyfile')
        os.chdir(buildPath)
        utils.system("doxygen %s" % doxyFile)
        return True

    def install(self):
        srcdir = os.path.join(self.buildDir(),'html')
        destdir = os.path.join(self.imageDir(),'share','doc','emerge','html')
        utils.copyDir(srcdir,destdir)
        return True

    def qmerge(self):
        if not PackageBase.qmerge(self):
            return False
        destdir = os.path.join(self.mergeDestinationDir(),'share','doc','emerge','html')
        utils.system("start %s/index.html" % destdir)
        return True

    def createPackage(self):
        return True

if __name__ == '__main__':
    Package().execute()
