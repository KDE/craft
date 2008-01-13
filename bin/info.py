# this module contains the information class

class infoclass:
    def __init__( self, RAW="" ):
        """ """
        self.targets = dict()
        self.svnTargets = dict()
        self.hardDependencies = dict()
        self.softDependencies = dict()
        self.defaultTarget = 'svnHEAD'
        self.buildTarget = 'svnHEAD'
        
        for x in RAW.splitlines():
            if not x == '':
                """ if version is not available then set it as -1 """
                self.hardDependencies[ x ] = [ -1 ]
        

        self.setDependencies()
        self.setTargets()
        self.setSVNTargets()

    def setDependencies( self ):
        """ """

    def setTargets( self ):
        """ """

    def setSVNTargets( self ):
        """ """
