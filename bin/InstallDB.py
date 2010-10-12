import os
import utils
from portage import *
import sqlite3

class InstallDB:
    def __init__( self, filename = os.path.join( etcDir(), 'install.db' ) ):
        self.dbfilename = filename
        if not os.path.exists( filename ):
            utils.debug( "database does not exist yet: creating database & importing old data" )
            self._prepareDatabase()
        else:
            utils.debug( "found database", 1 )
            self.connection = sqlite3.connect( self.dbfilename )
    
    def isInstalled( self, category, package, version='', prefix='' ):
        cmd = '''SELECT * FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append(prefix)
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append(category)
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append(package)
            parametersUsed = True

        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple(params) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute(cmd, tuple(params))
        isPackageInstalled = len(cursor.fetchall()) > 0
        if isPackageInstalled:
            utils.debug( "The package %s/%s has been installed in prefix '%s' with version '%s'." % (category, package, prefix, version), 1 )
        else:
            utils.debug( "Couldn't find a trace that the package %s/%s has been installed in prefix '%s' with version '%s'" % (category, package, prefix, version), 1 )
        cursor.close()
        return isPackageInstalled
        
    def findInstalled( self, category, package, prefix='' ):
        pass

    def getInstalled( self, package='', category='', prefix='' ):
        cmd = '''SELECT category, packageName, version, prefix FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append(prefix)
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append(category)
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append(package)
            parametersUsed = True

        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple(params) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute(cmd, tuple(params))
        values = cursor.fetchall()
        for entry in values:
            utils.debug( "entry: %s" % str(entry), 1 )
        cursor.close()
        return values

    def addInstalled( self, category, package, version, prefix='' ):
        if self.isInstalled( category, package, version, prefix ):
            return

        cursor = self.connection.cursor()
        params = [None, prefix, category, package, version]
        cmd = '''INSERT INTO packageList VALUES (?, ?, ?, ?, ?)'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple(params) ), 1 )
        cursor.execute(cmd, tuple(params))
        self.connection.commit()
        cursor.close()
        return
        
    def remInstalled( self, category, package, version, prefix='' ):
        cmd = '''DELETE FROM packageList'''
        params = []
        parametersUsed = False
        if not prefix == '' or not category == '' or not package == '':
            cmd += ''' WHERE'''

        if not prefix == '':
            cmd += ''' prefix=?'''
            params.append(prefix)
            parametersUsed = True

        if not category == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' category=?'''
            params.append(category)
            parametersUsed = True

        if not package == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' packageName=?'''
            params.append(package)
            parametersUsed = True

        if not version == '':
            if parametersUsed:
                cmd += ''' AND'''
            cmd += ''' version=?'''
            params.append(version)
            parametersUsed = True

        cmd += ''';'''
        utils.debug( "executing sqlcmd '%s' with parameters: %s" % ( cmd, tuple(params) ), 1 )
        
        cursor = self.connection.cursor()
        cursor.execute(cmd, tuple(params))
        cursor.close()
        
    def _prepareDatabase( self ):
        self.connection = sqlite3.connect( self.dbfilename )
        cursor = self.connection.cursor()

        # first, create the required table
        cursor.execute('''CREATE TABLE packageList (packageId INTEGER PRIMARY KEY AUTOINCREMENT, prefix TEXT, category TEXT, packageName TEXT, version TEXT)''')
        self.connection.commit()

        cursor.close()

    def _importExistingDatabase( self ):
        for category, package, version in PortageInstance.getInstallables():
            if self._isInstalled(category, package, version):
                utils.debug('adding installed package %s/%s-%s' % (category, package, version))
                self.addInstalled(category, package, version)



    def _isInstalled( self, category, package, version, buildType='' ):
        """ check if a package with a certain category, package and version is currently installed """

        # find in old style database
        path = etcDir()
        fileName = os.path.join(path,'installed')
        if not os.path.isfile( fileName ):
            return False

        found = False
        f = open( fileName, "rb" )
        for line in f.read().splitlines():
            (_category, _packageVersion) = line.split( "/" )
            (_package, _version) = packageSplit(_packageVersion)
            if category <> '' and version <> '' and category == _category and package == _package and version == _version:
                found = True
                break
            elif category == '' and version == '' and package == _package:
                found = True
                break
        f.close()

        # find in release mode database
        if not found and buildType <> '': 
            fileName = os.path.join(path,'installed-' + buildType )
            if os.path.isfile( fileName ):
                f = open( fileName, "rb" )
                for line in f.read().splitlines():
                    (_category, _packageVersion) = line.split( "/" )
                    (_package, _version) = packageSplit(_packageVersion)
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

        fileName = os.path.join( etcDir(), "installed" )
        if ( not os.path.isfile( fileName ) ):
            return None

        ret = None
        f = open( fileName, "rb" )
        str = "^%s/%s-(.*)$" % ( category, re.escape(package) )
        regex = re.compile( str )
        for line in f.read().splitlines():
            match = regex.match( line )
            if match:
                utils.debug( "found: " + match.group(1), 2 )
                ret = match.group(1)
        f.close()
        return ret;

    def _addInstalled( self, category, package, version, buildType='' ):
        """ add a package to the old style installation database in etc/portage/installed """

        utils.debug( "addInstalled called", 2 )
        # write a line to etc/portage/installed,
        # that contains category/package-version
        path = os.path.join( etcDir() )
        if ( not os.path.isdir( path ) ):
            os.makedirs( path )
        if buildType <> '': 
            fileName = 'installed-' + buildType
        else:
            fileName = 'installed'
        utils.debug("installing package %s - %s into %s" % (package, version, fileName), 2)
        if( os.path.isfile( os.path.join( path, fileName ) ) ):
            f = open( os.path.join( path, fileName ), "rb" )
            for line in f:
                if line.startswith( "%s/%s-%s" % ( category, package, version) ):
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
        utils.debug("removing package %s - %s from %s" % (package, version, fileName), 2)
        dbfile = os.path.join( etcDir(), fileName )
        tmpdbfile = os.path.join( etcDir(), "TMPinstalled" )
        found=False
        if os.path.exists( dbfile ):
            file = open( dbfile, "rb" )
            tfile = open( tmpdbfile, "wb" )
            for line in file:
                ## \todo the category should not be part of the search string 
                ## because otherwise it is not possible to unmerge package using 
                ## the same name but living in different categories
                if not line.startswith("%s/%s" % ( category, package ) ):
                    tfile.write( line )
                else:
                    found=True
            file.close()
            tfile.close()
            os.remove( dbfile )
            os.rename( tmpdbfile, dbfile )
        return found



if __name__ == '__main__':
    db_temp = InstallDB()
    db = InstallDB("C:/kde/kde-msvc/temp.db")
    utils.debug( 'testing installation database' )
    
    utils.debug( 'testing if package win32libs-sources/dbus-src with version 1.4.0 is installed:' )
    utils.debug( db._isInstalled('win32libs-sources', 'dbus-src', '1.4.0') )

    db.addInstalled('win32libs-sources', 'dbus-src', '1.4.0', 'release')
    db.getInstalled()
    db.getInstalled(category='win32libs-sources', prefix='debug')
    db.getInstalled(package='dbus-src')
    print db.getInstalled('dbus-src', 'win32libs-sources', 'release')
    db.isInstalled('win32libs-sources', 'dbus-src')
    db.remInstalled('win32libs-sources', 'dbus-src', '1.4.0')
    print db.getInstalled('dbus-src', 'win32libs-sources', 'release')

    db_temp._importExistingDatabase()
    print db_temp.getInstalled()