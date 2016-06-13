import EmergeDebug
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "Breeze icon theme."


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    #def cleanImage( self ):
     #   return True

    def resolveGitSymLink(self, path):
        if not os.path.exists(path):
            return path
        with open(path) as f:
            line = f.readline()
        newPath = os.path.join(os.path.split(path)[0], line)
        if os.path.exists(newPath):
            return self.resolveGitSymLink(newPath)
        return path

    def install( self):
        if not CMakeBuildSystem.install(self):
            return False
        for root, _, svgs in os.walk(self.imageDir(), ):
            for svg in svgs:
                path = os.path.join( root, svg)
                if path.endswith(".svg") and os.path.isfile(path):
                    toReplace = self.resolveGitSymLink(path)
                    if not os.path.exists(toReplace):
                        EmergeDebug.warning("Resolving %s failed: %s does not exists." % (path, toReplace))
                        continue
                    if toReplace != path:
                        utils.deleteFile(path)
                        utils.copyFile( toReplace, path)

        return True
