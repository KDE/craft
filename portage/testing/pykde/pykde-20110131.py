import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:pykde4'
        self.defaultTarget = 'gitHEAD'
        self.patchToApply['gitHEAD'] = ('pykde-20110318.patch', 1)

    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
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
            pyqtDir = os.path.join(self.rootdir,'lib','site-packages')
            if pyqtDir not in os.getenv("PYTHONPATH").split(';'):
                newPath = ";".join([os.getenv("PYTHONPATH"), pyqtDir])
                os.environ["PYTHONPATH"] = newPath
                utils.debug('added %s to PYTHONPATH' % pyqtDir, 2)

if __name__ == '__main__':
    Package().execute()
