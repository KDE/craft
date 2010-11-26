import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/emerge'
        self.svnTargets['refactoring-2010'] = 'branches/work/emerge/refactoring-2010'
        self.svnTargets['1.0'] = 'tags/emerge/1.0'
        self.defaultTarget = 'svnHEAD'
        
    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['dev-util/doxygen'] = 'default'

from Package.PackageBase import *
from Source.SvnSource import *
from BuildSystem.BuildSystemBase import *
from datetime import date

class Package(PackageBase,SvnSource,BuildSystemBase):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        SvnSource.__init__(self)
        BuildSystemBase.__init__(self,"")
        print self.subinfo.dependencies

    def checkoutDir(self, index=0 ): 
        return os.path.join(ROOTDIR,"emerge")

    def configure(self):
        doxygenSourcePathes = "%s %s" % (os.path.join(self.checkoutDir(),'bin'),os.path.join(self.checkoutDir(),'doc'))

        # copy and patch template
        sourceDoxyFile = os.path.join(self.checkoutDir(),'doc','Doxyfile')
        destPath = os.path.join(self.buildDir(),'doc')
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
        buildPath = os.path.join(self.buildDir(),'doc')
        doxyFile = os.path.join(buildPath,'Doxyfile')
        os.chdir(buildPath)
        utils.system("doxygen %s" % doxyFile)
        return True
        
    def install(self): 
        return True

    def qmerge(self):
        return True

    def createPackage(self):
        return True

if __name__ == '__main__':
    Package().execute()
