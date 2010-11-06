import os;
import utils;
import portage;
import emergePlatform;
import portage_versions;
import sqlite3;

def isDBEnabled():
    """ this function returns whether sqlite database should be used """
    return ( os.getenv( "EMERGE_ENABLE_SQLITEDB" ) == "True" )

class InstallPackage:
    """ InstallPackage finalizes an installation.

        If you call addInstalled or remInstalled an InstallPackage object is returned which
        you can use to handle file information with the InstallDB. For installation use code
        similar to this one:

        # get an InstallPackage object p
        p = InstallDB.installdb.addInstalled( "cat", "pac", "ver", "prefix" )
        # add files ( including the hash )
        p.addFiles( [ ( "file1", "hash1" ), ( "file2", "hash2" ), ( "file3", "hash3" ) ] )
        if failed:
            # in case we somehow need to go back
            p.revert()
        else:
            # finalize the installation
            p.install()

        Deinstallation works similar:
        p = InstallDB.installdb.remInstalled( "cat", "pac", "ver", "prefix" )
        # get the files ( including the hash )
        f = p.getFiles()
        # f now contains [ ( "file1", "hash1" ), ( "file2", "hash2" ), ( "file3", "hash3" ) ]
        if failed:
            # in case we somehow need to go back
            p.revert()
        else:
            # finalize the uninstall
            p.uninstall()
    """

    def __init__( self, cursor, packageId ):
        self.cursor = cursor
        self.packageId = packageId
        self.fileDict = dict()

    def addFiles( self, fileDict ):
        """ appends files to the list of files to be installed """
        self.fileDict.update( fileDict )

    def getFiles( self ):
        """ get a list of files that will be uninstalled """
        cmd = '''SELECT filename, fileHash FROM fileList WHERE packageId=?;'''
        utils.debug( "executing sqlcmd '%s' with parameter %s" % ( cmd, str( self.packageId ) ), 1 )
        self.cursor.execute(cmd, (self.packageId,))
        return self.cursor.fetchall()

    def revert( self ):
        """ revert all changes made to the database, use with care """
        self.cursor.connection.rollback()

    def uninstall( self ):
        """ really uninstall that package """
        cmd = '''DELETE FROM fileList WHERE packageId=?;'''
        utils.debug( "executing sqlcmd '%s' with parameter %s" % ( cmd, str( self.packageId ) ), 1 )
        self.cursor.execute(cmd, (self.packageId,))
        cmd = '''DELETE FROM packageList WHERE packageId=?;'''
        utils.debug( "executing sqlcmd '%s' with parameter %s" % ( cmd, str( self.packageId ) ), 1 )
        self.cursor.execute(cmd, (self.packageId,))
        self.cursor.connection.commit()

    def install( self ):
        """ marking the package & package file list installed """
        fileNumber = len( self.fileDict )
        # keys() and values will stay in the same order if no changes are done in between calls
        # structure of each tuple:
        # fileId | packageId == package Id | filenames | file hashes
        dataList = zip( [ None ] * fileNumber, [ self.packageId ] * fileNumber, self.fileDict.keys(), self.fileDict.values() )

        cmd = '''INSERT INTO fileList VALUES (?, ?, ?, ?)'''
        utils.debug( "executing sqlcmd '%s' %s times" % ( cmd, len( self.fileDict ) ), 1 )
        self.cursor.executemany( cmd, dataList )

        # at last, commit all the changes so that they are committed only after everything is written to the
        # database
        self.cursor.connection.commit()


class InstallDB:
    """ a database object which provides the methods for adding and removing a package and 
        checking its installation status.
        In case the database doesn't exist if the constructor is called, a new database is constructed
    """

    def __init__( self, filename = os.path.join( portage.etcDir(), 'install.db' ) ):
        self.dbfilename = filename
        if not os.path.exists( filename ):
            if not os.path.exists( portage.etcDir() ):
                os.makedirs( portage.etcDir() )
            utils.debug( "database does not exist yet: creating database & importing old data" )
            self._prepareDatabase()
        else:
            utils.debug( "found database", 1 )
            self.connection = sqlite3.connect( self.dbfilename )
    
    def getLastId( self ):
        """ returns the last id from a table, which is essentially the  """
        cmd = '''SELECT max(packageId) FROM packageList;'''
        
        cursor = self.connection.cursor()
        cursor.execute( cmd )
        lastId = cursor.fetchall()[0]
        return lastId[0]
        
    def __constructWhereStmt( self, _dict ):
        params = []
        parametersUsed = False
        stmt = ""
#        if not prefix == '' or not category == '' or not package == '':
#            cmd += ''' WHERE'''
#
        for key in _dict.keys():
            if not _dict[ key ] == None:
                if parametersUsed:
                    stmt += ''' AND'''
                stmt += ''' %s=?''' % key
                params.append( _dict[ key ] )
                parametersUsed = True
        if not stmt == "":
            stmt = ''' WHERE''' + stmt

        return stmt, params

    def isInstalled( self, category, package, version=None, prefix=None ):
        """ returns whether a package is installed. If version and prefix are empty, all versions 
            and prefixes will be checked. """
        cmd = '''SELECT * FROM packageList'''
        
        stmt, params = self.__constructWhereStmt( { 'prefix': prefix, 'category': category, 'packageName': package } )
        cmd += stmt
        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute( cmd, tuple( params ) )
        isPackageInstalled = len( cursor.fetchall() ) > 0
        if isPackageInstalled:
            utils.debug( """The package %s/%s has been installed in prefix '%s' with 
                            version '%s'.""" % ( category, package, prefix, version ), 1 )
        else:
            utils.debug( """Couldn't find a trace that the package %s/%s has been installed in 
                            prefix '%s' with version '%s'""" % ( category, package, prefix, version ), 1 )
        cursor.close()
        return isPackageInstalled
        
    def findInstalled( self, category, package, prefix=None ):
        """ get the version of a package that is installed """
        f = self.getInstalled( category, package, prefix )
        if len(f) == 3:
            return f[ 2 ]
        else:
            return None

    def getInstalled( self, category=None, package=None, prefix=None ):
        """ returns a list of the installed packages, which can be restricted by adding
            package, category and prefix.
        """
        cmd = '''SELECT category, packageName, version, prefix FROM packageList'''
        stmt, params = self.__constructWhereStmt( { 'prefix': prefix, 'category': category, 'packageName': package } )
        cmd += stmt
        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute( cmd, tuple( params ) )
        values = cursor.fetchall()
        cursor.close()
        return values

    def getPackageIds( self, category=None, package=None, version=None, prefix=None ):
        """ returns a list of the ids of the packages, which can be restricted by adding
            package, category and prefix.
        """
        cmd = '''SELECT packageId FROM packageList'''
        stmt, params = self.__constructWhereStmt( { 'prefix': prefix, 'category': category, 'packageName': package, 'version': version } )
        cmd += stmt
        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute( cmd, tuple( params ) )
        values = []
        for row in cursor:
            values.append( row[0] )
        return values

    def addInstalled( self, category, package, version, prefix=None, ignoreInstalled=False ):
        """ adds an installed package """
        cursor = self.connection.cursor()
        if self.isInstalled( category, package, version, prefix ) and not ignoreInstalled:
            raise Exception( 'package %s/%s-%s already installed (prefix %s)' % ( category, package, version, prefix ) )

        params = [ None, prefix, category, package, version ]
        cmd = '''INSERT INTO packageList VALUES (?, ?, ?, ?, ?)'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        cursor.execute( cmd, tuple( params ) )
        return InstallPackage( cursor, self.getLastId() )
        
    def remInstalled( self, category, package, version, prefix=None ):
        """ removes an installed package """
        cmd = '''DELETE FROM packageList'''
        stmt, params = self.__constructWhereStmt( { 'prefix': prefix, 'category': category, 'packageName': package, 'version': version } )
        cmd += stmt
        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        packageId = self.getLastId()
        cursor = self.connection.cursor()
        return [ InstallPackage( cursor, id ) for id in self.getPackageIds( category, package, version, prefix ) ]
        
    def _prepareDatabase( self ):
        """ prepare a new database and add the required table layout """
        self.connection = sqlite3.connect( self.dbfilename )
        cursor = self.connection.cursor()

        # first, create the required tables
        cursor.execute( '''CREATE TABLE packageList (packageId INTEGER PRIMARY KEY AUTOINCREMENT,
                           prefix TEXT, category TEXT, packageName TEXT, version TEXT)''' )
        cursor.execute( '''CREATE TABLE fileList (fileId INTEGER PRIMARY KEY AUTOINCREMENT,
                           packageId INTEGER, filename TEXT, fileHash TEXT)''' )
        self.connection.commit()
        
        self._importExistingDatabase()

    def _importExistingDatabase( self ):
        """ imports from the previous installation database system """
        for category, package, version in portage.PortageInstance.getInstallables():
            # FIXME: we need to adapt this to use prefixes as well
            utils.debug( "importing package %s/%s-%s ..." % ( category, package, version ) )
            if self._isInstalled( category, package, version ):
                utils.debug( 'adding installed package %s/%s-%s' % ( category, package, version ), 1 )
                packageObject = self.addInstalled( category, package, version )
                packageObject.addFiles( utils.getFileListFromManifest( os.getenv( "KDEROOT" ), package ) )
                packageObject.install()
                if emergePlatform.isCrossCompilingEnabled():
                    targetObject = self.addInstalled( category, package, version, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                    targetObject.addFiles( utils.getFileListFromManifest( os.path.join( os.getenv( "KDEROOT" ), os.getenv( "EMERGE_TARGET_PLATFORM" ) ), package ) )
                    targetObject.install()
                # check PackageBase.mergeDestinationDir() for further things regarding the import from other prefixes
                



    def _isInstalled( self, category, package, version, buildType='' ):
        """ check if a package with a certain category, package and version is installed (used for import) """

        # find in old style database
        path = portage.etcDir()
        fileName = os.path.join( path, 'installed' )
        if not os.path.isfile( fileName ):
            return False

        found = False
        f = open( fileName, "rb" )
        for line in f.read().splitlines():
            ( _category, _packageVersion ) = line.split( "/" )
            ( _package, _version ) = portage.packageSplit(_packageVersion)
            if category <> '' and version <> '' and category == _category and package == _package \
                              and version == _version:
                found = True
                break
            elif category == '' and version == '' and package == _package:
                found = True
                break
        f.close()

        # find in release mode database
        if not found and buildType <> '': 
            fileName = os.path.join( path,'installed-' + buildType )
            if os.path.isfile( fileName ):
                f = open( fileName, "rb" )
                for line in f.read().splitlines():
                    ( _category, _packageVersion ) = line.split( "/" )
                    ( _package, _version ) = portage.packageSplit( _packageVersion )
                    if category <> '' and version <> '' and category == _category and package == _package and version == _version:
                        found = True
                        break
                    elif category == '' and version == '' and package == _package:
                        found = True
                        break
                f.close()
        return found

# get a global object
if isDBEnabled():
    installdb = InstallDB()

# Testing the class
if __name__ == '__main__':
    # add two databases
    tempdbpath1 = os.path.join( os.getenv("KDEROOT"), "tmp", "temp1.db" )
    tempdbpath2 = os.path.join( os.getenv("KDEROOT"), "tmp", "temp2.db" )

    if not os.path.exists( os.path.join( os.getenv( "KDEROOT" ), "tmp" ) ):
        os.makedirs( os.path.join( os.getenv( "KDEROOT" ), "tmp" ) )

    if os.path.exists( tempdbpath1 ):
        os.remove( tempdbpath1 )
    if os.path.exists( tempdbpath2 ):
        os.remove( tempdbpath2 )

    db_temp = InstallDB( tempdbpath1 )
    db = InstallDB( tempdbpath2 )

    utils.debug( 'testing installation database' )
    
    utils.debug( 'testing if package win32libs-sources/dbus-src with version 1.4.0 is installed: %s' % 
                 db._isInstalled( 'win32libs-sources', 'dbus-src', '1.4.0' ) )

    # in case the package is still installed, remove it first silently
    if db.isInstalled( 'win32libs-sources', 'dbus-src', '1.4.0' ):
        packageList = db.remInstalled( 'win32libs-sources', 'dbus-src', '1.4.0' )
        # really commit uninstall
        for package in packageList:
            package.uninstall()
    utils.debug_line()

    utils.new_line()
    # add a package
    utils.debug( 'installing package win32libs-sources/dbus-src-1.4.0 (release)' )
    package = db.addInstalled( 'win32libs-sources', 'dbus-src', '1.4.0', 'release' )
    package.addFiles( dict().fromkeys( [ 'test', 'test1', 'test2' ], 'empty hash' ) )
    # now really commit the package
    package.install()
    
    # add another package in a different prefix
    utils.debug( 'installing package win32libs-sources/dbus-src-1.4.0 (debug)' )
    package = db.addInstalled( 'win32libs-sources', 'dbus-src', '1.4.0', 'debug' )
    package.addFiles( dict().fromkeys( [ 'test', 'test1', 'test2' ], 'empty hash' ) )
    # now really commit the package
    package.install()
    utils.debug_line()
    
    utils.new_line()
    utils.debug( 'checking installed packages' )
    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'debug' ) )

    utils.new_line()
    utils.debug( 'now trying to remove package & revert it again later' )
    # remove the package again
    packageList = db.remInstalled( 'win32libs-sources', 'dbus-src', '1.4.0' )
    for pac in packageList:
        for line in pac.getFiles():
            # we could remove the file here
            # print line
            pass
    utils.debug_line()

    utils.new_line()
    utils.debug( 'checking installed packages' )
    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'debug' ) )
    utils.debug_line()
    
    utils.new_line()
    utils.debug( 'reverting removal' )
    # now instead of completing the removal, revert it
    for pac in packageList:
        pac.revert()

    utils.debug( 'checking installed packages' )
    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'debug' ) )
    utils.debug_line()

    db.getInstalled()
    db.getInstalled( category='win32libs-sources', prefix='debug' )
    db.getInstalled( package='dbus-src' )
    
    utils.new_line()
    utils.debug( 'now really remove the package' )
    packageList = db.remInstalled( 'win32libs-sources', 'dbus-src', '1.4.0')
    for pac in packageList:
        utils.debug( 'removing %s files' % len( pac.getFiles() ) )
        pac.uninstall()

    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'win32libs-sources', 'dbus-src', 'debug' ) )
    utils.debug_line()

    # test the import from the old style (manifest based) databases
    utils.new_line()
    db_temp._importExistingDatabase()
    print "getInstalled:", db_temp.getInstalled()
    print "findInstalled:", portage.findInstalled( 'win32libs-sources', 'dbus-src' )
    print "getFileListFromManifest:", len( utils.getFileListFromManifest( os.getenv( "KDEROOT" ), 'dbus-src' ) )