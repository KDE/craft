#
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# mercurial support based on the git support

from Source.VersionSystemSourceBase import *

class HgSource ( VersionSystemSourceBase ):
    """mercurial support"""
    def __init__( self, subinfo=None ):
        utils.trace( 'HgSource __init__', 2 )
        if subinfo:
            self.subinfo = subinfo
        VersionSystemSourceBase.__init__( self )

        self.hgExecutable = os.path.join( os.environ.get( 'ProgramFiles' ), 'mercurial', 'hg.exe' )
        self.enableHg = os.path.exists( self.hgExecutable )
        # add other locations
        if not self.enableHg:
            print("could not find hg.exe, you should run emerge mercurial")
        # guard spaces in path
        self.hgExecutable = "\"%s\"" % self.hgExecutable

        # initialize the repository
        self.repo = None

    def fetch( self, repopath=None ):
        """try to clone or update the repository"""
        utils.trace( "HgSource.fetch called", 2 )

        # get the path where the repositories should be stored to
        if repopath == None:
            repopath = self.repositoryUrl()

        # in case you need to move from a read only Url to a writeable one, here it gets replaced
#        repoString = utils.replaceVCSUrl( repopath )
        repopath = repopath.replace("[hg]", "")
        repoUrl, repoBranch, _ = utils.splitVCSUrl( repopath )
        ret = True

        # only run if wanted (e.g. no --offline is given on the commandline) or no hg support is given by the python installation
        if ( not self.noFetch and self.enableHg ):
            # question whether mercurial stuff uses these proxies
            self.setProxy()
            checkoutDir = self.checkoutDir()

            # check corrupted checkout dir
            if os.path.exists( checkoutDir ) and not os.path.exists( checkoutDir + "\.hg" ):
                os.rmdir( checkoutDir )
            
            if not os.path.exists( checkoutDir ):
                os.makedirs( checkoutDir )
                os.chdir( checkoutDir )
                ret = self.system( "%s clone %s ." % ( self.hgExecutable, repoUrl ) ) # TODO: check return code for success
            
            if os.path.exists( checkoutDir ):
                os.chdir( checkoutDir )
                ret = self.system( "%s update %s" % ( self.hgExecutable, repoBranch ) ) # TODO: check return code for success
        else:
            utils.debug( "skipping hg fetch (--offline)" )
        return ret

    def applyPatch(self, fileName, patchdepth, unusedSrcDir=None):
        """apply a patch to a mercurial repository checkout"""
        utils.trace( "HgSource.applyPatches called", 2 )
        if fileName and self.enableHg:
            patchfile = os.path.join ( self.packageDir(), fileName )
            os.chdir( self.sourceDir() )
            return self.system( '"%s" import -p %s "%s"' % (self.hgExecutable, patchdepth, patchfile) )
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir. The patch file is named autocreated.patch"""
        utils.trace( "HgSource.createPatch called", 2 )
        ret = False
        if self.enableHg:
            os.chdir( self.sourceDir() )
            patchFile = os.path.join( self.packageDir(), "%s-%s.patch" % ( self.package, str( datetime.date.today() ).replace('-', '') ) )
            ret = self.system( self.sourceDir(), "%s diff > %s" % ( self.hgExecutable,  patchFile ) )
        return ret

    def sourceVersion( self ):
        """ return the revision of the repository """
        utils.trace( "HgSource.sourceVersion called", 2 )

        if self.enableHg:

            # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
            with open( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergehgtip.tmp" ), "wb+" ) as tempfile:

                # run the command
                utils.system( "%s tip" % self.hgExecutable, stdout=tempfile )
                # TODO: check return value for success
                tempfile.seek( os.SEEK_SET )

                # read the temporary file and grab the first line
                revision = tempfile.readline().replace("changeset:", "").strip()

            os.remove( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergehgtip.tmp" ) )
        # always return True to not break something serious
        return revision
