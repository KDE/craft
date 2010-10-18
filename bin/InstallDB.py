import os
import utils
import portage
import portage_versions
import sqlite3

class InstallPackage:
    """ install package finalizes an installation """
    def __init__( self, cursor, packageId ):
        self.cursor = cursor
        self.packageId = packageId
        self.fileDict = dict()

    def addFiles( self, fileDict ):
        """ appending files to the list of files to be installed """
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
    """
    def __init__( self, filename = os.path.join( portage.etcDir(), 'install.db' ) ):
        self.dbfilename = filename
        if not os.path.exists( filename ):
            utils.debug( "database does not exist yet: creating database & importing old data" )
            self._prepareDatabase()
        else:
            utils.debug( "found database", 1 )
            self.connection = sqlite3.connect( self.dbfilename )
    
    def getLastId( self ):
        """ returns the last id from a table """
        cmd = '''SELECT max(packageId) FROM packageList;'''
        
        cursor = self.connection.cursor()
        cursor.execute( cmd )
        lastId = cursor.fetchall()[0]
        return lastId[0]
        
    def isInstalled( self, category, package, version='', prefix='' ):
        """ returns whether a package is installed. If version and prefix are empty, all versions 
            and prefixes will be checked. """
        cmd = '''SELECT * FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append( prefix )
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append( category )
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append( package )
            parametersUsed = True

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
                            prefix '%s' with version '%s'""" % (category, package, prefix, version), 1 )
        cursor.close()
        return isPackageInstalled
        
    def findInstalled( self, category, package, prefix='' ):
        pass

    def getInstalled( self, package='', category='', prefix='' ):
        """ returns a list of the installed packages, which can be restricted by adding
            package, category and prefix.
        """
        cmd = '''SELECT category, packageName, version, prefix FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append( prefix )
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append( category )
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append( package )
            parametersUsed = True

        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute( cmd, tuple( params ) )
        values = cursor.fetchall()
        cursor.close()
        return values

    def getPackageIds( self, category='', package='', version='', prefix='' ):
        """ returns a list of the ids of the packages, which can be restricted by adding
            package, category and prefix.
        """
        cmd = '''SELECT packageId FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append( prefix )
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append( category )
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append( package )
            parametersUsed = True

        if not version == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' version=?'''
            params.append( version )
            parametersUsed = True

        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute( cmd, tuple( params ) )
        values = []
        for row in cursor:
            values.append( row[0] )
        return values

    def addInstalled( self, category, package, version, prefix='' ):
        """ adds an installed package """
        if self.isInstalled( category, package, version, prefix ):
            raise Exception( 'package %s/%s-%s already installed (prefix %s)' % ( category, package, version, prefix ) )

        cursor = self.connection.cursor()
        params = [ None, prefix, category, package, version ]
        cmd = '''INSERT INTO packageList VALUES (?, ?, ?, ?, ?)'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        cursor.execute( cmd, tuple( params ) )
        return InstallPackage( cursor, self.getLastId() )
        
    def remInstalled( self, category, package, version, prefix='' ):
        """ removes an installed package """
        cmd = '''DELETE FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append( prefix )
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append( category )
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append( package )
            parametersUsed = True

        if not version == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' version=?'''
            params.append( version )
            parametersUsed = True

        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple( params ) ), 1 )
        
        packageId = self.getLastId()
        cursor = self.connection.cursor()
        return [ InstallPackage( cursor, id ) for id in self.getPackageIds( category, package, version, prefix ) ]
        
    def _prepareDatabase( self ):
        self.connection = sqlite3.connect( self.dbfilename )
        cursor = self.connection.cursor()

        # first, create the required tables
        cursor.execute( '''CREATE TABLE packageList (packageId INTEGER PRIMARY KEY AUTOINCREMENT,
                           prefix TEXT, category TEXT, packageName TEXT, version TEXT)''' )
        cursor.execute( '''CREATE TABLE fileList (fileId INTEGER PRIMARY KEY AUTOINCREMENT,
                           packageId INTEGER, filename TEXT, fileHash TEXT)''' )
        self.connection.commit()

        cursor.close()

    def _importExistingDatabase( self ):
        """ imports from the previous installation database system """
        for category, package, version in portage.PortageInstance.getInstallables():
            if self._isInstalled( category, package, version ):
                utils.debug( 'adding installed package %s/%s-%s' % ( category, package, version ), 1 )
                packageObject = self.addInstalled( category, package, version )
                packageObject.addFiles(utils.getFileListFromManifest( os.getenv( "KDEROOT" ), package ) )
                packageObject.install()


    def _isInstalled( self, category, package, version, buildType='' ):
        """ check if a package with a certain category, package and version is installed """

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

#        if ( not found ):
#            """ try to detect packages from the installer """
#            bin = utils.checkManifestFile( os.path.join( os.getenv( "KDEROOT" ), "manifest", package + "-" + version + "-bin.ver"), category, package, version )
#            lib = utils.checkManifestFile( os.path.join( os.getenv( "KDEROOT" ), "manifest", package + "-" + version + "-lib.ver"), category, package, version )
#            found = found or bin or lib
#
#        if ( not found and os.getenv( "EMERGE_VERSIONING" ) == "False" or os.getenv( "EMERGE_SOURCEONLY" ) == "True" ):
#            """ check for any installation """
#            if not os.path.exists(os.path.join( os.getenv( "KDEROOT" ), "manifest" ) ):
#                return False
#            if package.endswith( "-src" ):
#                package = package[:-4]
#            for filename in os.listdir( os.path.join( os.getenv( "KDEROOT" ), "manifest" ) ):
#                if filename.startswith( package ):
#                    found = True
#                    break
        return found

    def _findInstalled( self, category, package, buildType='' ):
        """ find a package of a certain category and packagename and return the full install line """

        fileName = os.path.join( portage.etcDir(), "installed" )
        if ( not os.path.isfile( fileName ) ):
            return None

        ret = None
        f = open( fileName, "rb" )
        str = "^%s/%s-(.*)$" % ( category, re.escape( package ) )
        regex = re.compile( str )
        for line in f.read().splitlines():
            match = regex.match( line )
            if match:
                utils.debug( "found: " + match.group( 1 ), 2 )
                ret = match.group( 1 )
        f.close()
        return ret;

    def _addInstalled( self, category, package, version, buildType='' ):
        """ add a package to the old style installation database in etc/portage/installed """

        utils.debug( "addInstalled called", 2 )
        # write a line to etc/portage/installed,
        # that contains category/package-version
        path = os.path.join( portage.etcDir() )
        if ( not os.path.isdir( path ) ):
            os.makedirs( path )
        if buildType <> '': 
            fileName = 'installed-' + buildType
        else:
            fileName = 'installed'
        utils.debug( "installing package %s - %s into %s" % ( package, version, fileName ), 2 )
        if( os.path.isfile( os.path.join( path, fileName ) ) ):
            f = open( os.path.join( path, fileName ), "rb" )
            for line in f:
                if line.startswith( "%s/%s-%s" % ( category, package, version ) ):
                    utils.warning( "version already installed" )
                    return
                elif line.startswith( "%s/%s-" % ( category, package ) ):
                    utils.die( "already installed, this should no happen" )
        f = open( os.path.join( path, fileName ), "ab" )
        f.write( "%s/%s-%s\r\n" % ( category, package, version ) )
        f.close()

    def _remInstalled( self, category, package, version, buildType='' ):
        """ remove an installed package """

        utils.debug( "remInstalled called", 2 )
        if buildType <> '': 
            fileName = 'installed-' + buildType
        else:
            fileName = 'installed'
        utils.debug( "removing package %s - %s from %s" % ( package, version, fileName ), 2 )
        dbfile = os.path.join( portage.etcDir(), fileName )
        tmpdbfile = os.path.join( portage.etcDir(), "TMPinstalled" )
        found=False
        if os.path.exists( dbfile ):
            file = open( dbfile, "rb" )
            tfile = open( tmpdbfile, "wb" )
            for line in file:
                ## \todo the category should not be part of the search string 
                ## because otherwise it is not possible to unmerge package using 
                ## the same name but living in different categories
                if not line.startswith( "%s/%s" % ( category, package ) ):
                    tfile.write( line )
                else:
                    found=True
            file.close()
            tfile.close()
            os.remove( dbfile )
            os.rename( tmpdbfile, dbfile )
        return found



# Testing the class

if __name__ == '__main__':
    # add two databases, one default database, and a temporary one
    db_temp = InstallDB()
    db = InstallDB( "C:/kde/kde-msvc/temp.db" )
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
    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'debug' ) )

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
    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'debug' ) )
    utils.debug_line()
    
    utils.new_line()
    utils.debug( 'reverting removal' )
    # now instead of completing the removal, revert it
    for pac in packageList:
        pac.revert()

    utils.debug( 'checking installed packages' )
    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'debug' ) )
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

    utils.debug( 'get installed package (release): %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'release' ) )
    utils.debug( 'get installed package (debug):   %s' % db.getInstalled( 'dbus-src', 'win32libs-sources', 'debug' ) )
    utils.debug_line()

    # test the import from the old style (manifest based) databases
    utils.new_line()
    db_temp._importExistingDatabase()
    print "getInstalled:", db_temp.getInstalled()
    print "findInstalled:", portage.findInstalled( 'win32libs-sources', 'dbus-src' )
    print "getFileListFromManifest:", len( utils.getFileListFromManifest( 'C:/kde/kde-msvc', 'dbus-src' ) )