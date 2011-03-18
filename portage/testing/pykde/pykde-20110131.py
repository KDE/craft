import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:pykde4'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.6/kdelibs'] = '4.6.0'
        self.hardDependencies['testing/sip'] = 'default'
        self.hardDependencies['testing/pyqt'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        localPythonPath = os.path.join(self.rootdir, 'emerge', 'python')
        haveLocalPython = os.path.exists(localPythonPath)
        if haveLocalPython:
            self.subinfo.options.merge.destinationPath = "emerge/python"
        else:
            # PyQt4 does not install itself in C:\Python27\Lib\site-packages
            # so how is python supposed to be able to import it?
            # TODO: this is a wild hack...
            pyqtDir = os.path.join(self.rootdir,'build','testing','pyqt-4.8.3',
                    'image-mingw4-Debug-4.8.3','Lib','site-packages')
            if pyqtDir not in os.getenv("PYTHONPATH").split(';'):
                newPath = ";".join([os.getenv("PYTHONPATH"), pyqtDir])
                os.environ["PYTHONPATH"] = newPath
                utils.debug('special PYTHONPATH for pykde, so we can import PyQt4: %s' % newPath)

if __name__ == '__main__':
    Package().execute()
