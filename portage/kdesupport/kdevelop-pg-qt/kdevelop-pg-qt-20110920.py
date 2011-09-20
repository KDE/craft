import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdevelop-pg-qt'
        self.shortDescription = "Lexer- and parser-generator for C++. It generates recursive-descent-LL(1)-parsers and unicode-aware lexers."
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()

if __name__ == '__main__':
    Package().execute()
