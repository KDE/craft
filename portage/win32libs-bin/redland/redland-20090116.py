import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.0.8']:
            self.targets[ version ] = repoUrl + """/redland-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/redland-""" + version + """-lib.tar.bz2"""

            
        self.defaultTarget = '1.0.8'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/libcurl'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/pcre'] = 'default'
        self.hardDependencies['testing/sqlite'] = 'default'
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
