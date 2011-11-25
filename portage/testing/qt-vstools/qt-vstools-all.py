
import utils
import info
from Package.QMakePackageBase import *

# vs2010 help viewer api 
# http://www.microsoft.com/downloads/info.aspx?na=41&srcfamilyid=94ab4784-b7c3-49ac-a315-9688bc5c84c3&srcdisplaylang=en&u=http%3a%2f%2fdownload.microsoft.com%2fdownload%2fF%2fF%2fE%2fFFE071DC-CB61-41BE-BE61-21A0EFB4341B%2fHelpViewerSDK.EXE

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['HEAD'] = 'git://gitorious.org/qt-labs/vstools.git'
        self.svnTargets['TEMP'] = 'git@gitorious.org:~rhabacker/qt-labs/rhabackers-vstools.git'
        self.defaultTarget = 'HEAD'

    def setDependencies( self ):
        self.buildDependencies['libs/qt'] = 'default'


class Package(QMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
     
    def make( self ):
        if not QMakePackageBase.make( self ):
            return False
        cmd = "%s\\help\\createdoc.bat --qt" % self.sourceDir()
        return utils.system(cmd, cwd=self.buildDir())

if __name__ == '__main__':
    Package().execute()
