# 
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# mercurial support based on the git support

from VersionSystemSourceBase import *
import os
import utils
class HgSource ( VersionSystemSourceBase ):
    """mercurial support"""
    def __init__( self ):
        VersionSystemSourceBase.__init__( self )

        self.enableHg = True
        try:
            self.enableHg = self.system("hg help > NUL")
        except:
            self.enableHg = False

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
        [repoUrl, repoBranch, repoTag ] = utils.splitGitUrl( repopath )
        

        if utils.verbose() <= 2:
            devNull = " > NUL"
        else:
            devNull = ""
        ret = True

        # only run if wanted (e.g. no --offline is given on the commandline) or no hg support is given by the python installation
        if ( not self.noFetch and self.enableHg ):
            # question whether mercurial stuff uses these proxies
            self.setProxy()

            if os.path.exists( self.checkoutDir() ):
                # if directory already exists, simply do an update but obey to offline
                os.chdir( self.checkoutDir() )
                ret = self.system( "hg update" )
                
            else:
                # it doesn't exist so clone the repo
                svnsrcdir = self.checkoutDir().replace( self.package, "" )
                if not os.path.exists( svnsrcdir ):
                    os.makedirs( svnsrcdir )

                os.chdir( svnsrcdir )
                ret = self.system( "hg clone %s %s" % ( repoUrl, self.package ) )
        else:
            utils.debug( "skipping hg fetch (--offline)" )
        return ret
    
    def applyPatch(self, file, patchdepth):
        """apply a patch to a mercurial repository checkout"""
        utils.trace( "HgSource.applyPatches called", 2 )
        if file and self.enableHg:
            patchfile = os.path.join ( self.packageDir(), file )
            os.chdir( self.sourceDir() )
            return self.system( "hg import -p %s %s" % (patchdepth, patchfile) )
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir. The patch file is named autocreated.patch"""
        utils.trace( "HgSource.createPatch called", 2 )
        ret = False
        if self.enableHg:
            os.chdir( self.sourceDir() )
            ret = self.system( self.sourceDir(), "hg diff > %s" % os.path.join( self.packageDir(), "%s-%s.patch" % ( self.package, str( datetime.date.today() ).replace('-', '') ) ) )
        return ret

    def sourceVersion( self ):
        """ return the revision of the repository """
        utils.trace( "HgSource.sourceVersion called", 2 )

        if self.enableHg:
        
            # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
            tempfile = open( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergehgtip.tmp" ), "wb+" )
            
            # run the command
            ret = utils.system( "hg tip", tempfile )
            tempfile.seek( os.SEEK_SET )

            # read the temporary file and grab the first line
            revision = tempfile.readline().replace("changeset:", "").strip()
            tempfile.close()
            
            # print the revision - everything else should be quiet now
            print revision
            os.remove( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergehgtip.tmp" ) )
        # always return True to not break something serious
        return True
