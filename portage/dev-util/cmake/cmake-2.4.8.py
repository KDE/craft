import base
import info

SRC_URI= "http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip"

class subinfo( info.infoclass ):
    def setTargets( self ):
        """ """
        self.targets['2.4.8'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip'
        self.targets['2.5.0'] = 'http://www.cmake.org/files/vCVS/cmake-2.5.20080311-win32-x86.zip'
        self.targetInstSrc['2.4.8'] = 'cmake-2.4.8-win32-x86'
        self.targetInstSrc['2.5.0'] = 'cmake-2.5.20080311-win32-x86'
        self.defaultTarget = '2.4.8'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.instsrcdir = "cmake-2.4.8-win32-x86"
    self.subinfo = subinfo()
    if self.traditional:
      self.instdestdir = "cmake"

if __name__ == '__main__':
    subclass().execute()
