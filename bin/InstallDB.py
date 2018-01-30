import sqlite3

from CraftConfig import *
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs, TemporaryUseShortpath


class InstallPackage(object):
    """ InstallPackage finalizes an installation.

        If you call addInstalled or remInstalled an InstallPackage object is returned which
        you can use to handle file information with the InstallDB. For installation use code
        similar to this one:

        # get an InstallPackage object p
        p = CraftCore.installdb.addInstalled( "cat", "pac", "ver", "prefix" )
        # add files ( including the hash )
        p.addFiles( [ ( "file1", "hash1" ), ( "file2", "hash2" ), ( "file3", "hash3" ) ] )
        if failed:
            # in case we somehow need to go back
            p.revert()
        else:
            # finalize the installation
            p.install()

        Deinstallation works similar:
        p = CraftCore.installdb.remInstalled( "cat", "pac", "ver", "prefix" )
        # get the files ( including the hash )
        f = p.getFilesWithHashes()
        # f now contains [ ( "file1", "hash1" ), ( "file2", "hash2" ), ( "file3", "hash3" ) ]
        if failed:
            # in case we somehow need to go back
            p.revert()
        else:
            # finalize the uninstall
            p.uninstall()
    """

    def __init__(self, cursor, packageId):
        self.cursor = cursor
        self.packageId = packageId
        self.fileDict = dict()

    def addFiles(self, fileDict):
        """ appends files to the list of files to be installed """
        self.fileDict.update(fileDict)

    def getFilesWithHashes(self):
        """ get the list of files (filename, fileHash tuples) for the given package """
        cmd = '''SELECT filename, fileHash FROM fileList WHERE packageId=?;'''
        InstallDB.log("executing sqlcmd '%s' with parameter %s" % (cmd, str(self.packageId)))
        self.cursor.execute(cmd, (self.packageId,))
        return self.cursor.fetchall()

    def getFiles(self):
        """ get the list of files for the given package """
        cmd = '''SELECT filename FROM fileList WHERE packageId=?;'''
        InstallDB.log("executing sqlcmd '%s' with parameter %s" % (cmd, str(self.packageId)))
        self.cursor.execute(cmd, (self.packageId,))
        return self.cursor.fetchall()

    def getPackageInfo(self):
        cmd = '''SELECT packagePath, version FROM packageList WHERE packageId=?'''
        self.cursor.execute(cmd, (self.packageId,))
        return self.cursor.fetchall()[0]

    def revert(self):
        """ revert all changes made to the database, use with care """
        self.cursor.connection.rollback()

    def uninstall(self):
        """ really uninstall that package """
        cmd = '''DELETE FROM fileList WHERE packageId=?;'''
        InstallDB.log("executing sqlcmd '%s' with parameter %s" % (cmd, str(self.packageId)))
        self.cursor.execute(cmd, (self.packageId,))
        cmd = '''DELETE FROM packageList WHERE packageId=?;'''
        InstallDB.log("executing sqlcmd '%s' with parameter %s" % (cmd, str(self.packageId)))
        self.cursor.execute(cmd, (self.packageId,))
        self.cursor.connection.commit()

    def install(self):
        """ marking the package & package file list installed """
        fileNumber = len(self.fileDict)
        # keys() and values will stay in the same order if no changes are done in between calls
        # structure of each tuple:
        # fileId | packageId == package Id | filenames | file hashes
        dataList = list(zip([None] * fileNumber, [self.packageId] * fileNumber, list(self.fileDict.keys()),
                            list(self.fileDict.values())))

        cmd = '''INSERT INTO fileList VALUES (?, ?, ?, ?)'''
        InstallDB.log("executing sqlcmd '%s' %s times" % (cmd, len(self.fileDict)))
        self.cursor.executemany(cmd, dataList)

        # at last, commit all the changes so that they are committed only after everything is written to the
        # database
        self.cursor.connection.commit()

    def getRevision(self):
        self.cursor.execute("SELECT revision FROM packageList WHERE packageId == ?", (self.packageId,))
        return self.cursor.fetchall()[0][0]

    def getVersion(self):
        self.cursor.execute("SELECT version FROM packageList WHERE packageId == ?", (self.packageId,))
        return self.cursor.fetchall()[0][0]

    def getCacheVersion(self):
        self.cursor.execute("SELECT cacheVersion FROM packageList WHERE packageId == ?", (self.packageId,))
        return self.cursor.fetchall()[0][0]



class InstallDB(object):
    """ a database object which provides the methods for adding and removing a package and
        checking its installation status.
        In case the database doesn't exist if the constructor is called, a new database is constructed
    """
    SCHEMA_VERSION = 1

    def __init__(self, filename=None):
        if filename == None:
            with TemporaryUseShortpath(False):
                filename = os.path.join(CraftStandardDirs.etcBlueprintDir(), 'install.db')

        self.dbfilename = filename
        self._prepareDatabase()

    @staticmethod
    def log(command):
        if CraftCore.debug.verbose() > 0:
            CraftCore.log.debug(command)

    def getLastId(self):
        """ returns the last id from a table, which is essentially the  """
        cmd = '''SELECT max(packageId) FROM packageList;'''

        cursor = self.connection.cursor()
        cursor.execute(cmd)
        lastId = cursor.fetchall()[0]
        return lastId[0]

    def __constructWhereStmt(self, _dict):
        params = []
        parametersUsed = False
        stmt = ""
        for key in list(_dict.keys()):
            if _dict[key]:
                if parametersUsed:
                    stmt += ''' AND'''
                stmt += f''' {key}=?'''
                params.append(str(_dict[key]))
                parametersUsed = True
        if not stmt == "":
            stmt = ''' WHERE''' + stmt

        return stmt, params

    def isInstalled(self,  package, version=None):
        """ returns whether a package is installed. If version is empty, all versions will be checked. """
        cmd = '''SELECT * FROM packageList'''
        stmt, params = self.__constructWhereStmt(
            {'prefix': None, 'packagePath': package, 'version': version})
        cmd += stmt
        cmd += ''';'''
        InstallDB.log("executing sqlcmd '%s' with parameters: %s" % (cmd, tuple(params)))

        cursor = self.connection.cursor()
        cursor.execute(cmd, tuple(params))
        installedPackage  = cursor.fetchall()
        if installedPackage:
            InstallDB.log(f"""The package {package} has been installed with
                            version '{version}'.""")
        else:
            InstallDB.log(f"""Couldn't find a trace that the package {package} has been installed with version '{version}'""")
        cursor.close()
        return bool(installedPackage)

    def getDistinctInstalled(self, package=None):
        """ returns a list of the installed packages, which can be restricted by adding
            package.
        """
        cmd = '''SELECT DISTINCT packagePath, version FROM packageList'''
        stmt, params = self.__constructWhereStmt({'prefix': None, 'packagePath': package})
        cmd += stmt
        cmd += ''';'''
        InstallDB.log("executing sqlcmd '%s' with parameters: %s" % (cmd, tuple(params)))

        cursor = self.connection.cursor()
        cursor.execute(cmd, tuple(params))
        values = cursor.fetchall()
        cursor.close()
        return values

    def getPackageIds(self, package):
        """ returns a list of the ids of the packages, which can be restricted by adding
            package.
        """
        cmd = '''SELECT packageId FROM packageList'''
        stmt, params = self.__constructWhereStmt({'prefix': None, 'packagePath': package.path})
        cmd += stmt
        cmd += ''';'''
        InstallDB.log("executing sqlcmd '%s' with parameters: %s" % (cmd, tuple(params)))

        cursor = self.connection.cursor()
        cursor.execute(cmd, tuple(params))
        values = []
        for row in cursor:
            values.append(row[0])
        return values

    def getPackagesForFileSearch(self, filename):
        """ returns a list of tuple(InstallPackage(), filename) for packages providing a given file """

        cursor = self.connection.cursor()
        cmd = '''SELECT packageId, fileName FROM fileList WHERE filename LIKE ?;'''
        InstallDB.log("executing sqlcmd '%s' with parameter %s" % (cmd, str(filename)))
        cursor.execute(cmd, ("%" + filename + "%",))
        rows = cursor.fetchall()
        return [(InstallPackage(cursor, row[0]), row[1]) for row in rows]

    def addInstalled(self, package, version, ignoreInstalled=False, revision="", cacheVersion=None):
        """ adds an installed package """
        cursor = self.connection.cursor()
        if self.isInstalled(package, version) and not ignoreInstalled:
            raise Exception(f'package {package}-{version} already installed')
        params = (None, package.path, version, revision, cacheVersion)
        cmd = '''INSERT INTO packageList (packageId, packagePath, version, revision, cacheVersion) VALUES (?, ?, ?, ?, ?)'''
        InstallDB.log(f"executing sqlcmd {cmd!r} with parameters: {params}")
        cursor.execute(cmd, params)
        return InstallPackage(cursor, self.getLastId())

    def getInstalledPackages(self, package):
        """ return an installed package """
        cursor = self.connection.cursor()
        return [InstallPackage(cursor, pId) for pId in self.getPackageIds(package)]

    def _prepareDatabase(self):
        """ prepare a new database and add the required table layout """
        with TemporaryUseShortpath(False):
            if not os.path.exists(self.dbfilename):
                if not os.path.exists(CraftStandardDirs.etcBlueprintDir()):
                    os.makedirs(CraftStandardDirs.etcBlueprintDir())
                self.connection = sqlite3.connect(self.dbfilename)
                cursor = self.connection.cursor()

                # first, create the required tables
                cursor.execute('''CREATE TABLE packageList (packageId INTEGER PRIMARY KEY AUTOINCREMENT,
                                   prefix TEXT, packagePath TEXT, version TEXT, revision TEXT, cacheVersion TEXT)''')
                cursor.execute('''CREATE TABLE fileList (fileId INTEGER PRIMARY KEY AUTOINCREMENT,
                                   packageId INTEGER, filename TEXT, fileHash TEXT)''')
                cursor.execute(f'''PRAGMA user_version={InstallDB.SCHEMA_VERSION};''')
                self.connection.commit()
            else:
                self.connection = sqlite3.connect(self.dbfilename)
                self.__migrateDatabase()


    def __migrateDatabase(self):
        cursor = self.connection.cursor()
        cursor.execute('''PRAGMA user_version;''')
        version = cursor.fetchall()[0][0]
        # TODO: drop prefix from packageList (will break compat)
        if version < 1:
            cursor.execute('''ALTER TABLE packageList ADD COLUMN cacheVersion TEXT;''')
        cursor.execute(f'''PRAGMA user_version={InstallDB.SCHEMA_VERSION};''')


def printInstalled():
    """get all the packages that are already installed"""
    installed = CraftCore.installdb.getDistinctInstalled()
    width = 40
    def printLine(first, second):
        CraftCore.log.info(f"{first:{width}}: {second}")

    printLine("Package", "Version")
    printLine("=" * width, "=" * 10)
    installed = sorted(installed, key=lambda x :x[0])
    for package, version in installed:
        printLine(package, version)

def printPackagesForFileSearch(filename):
    packages = CraftCore.installdb.getPackagesForFileSearch(filename)
    for pId, filename in packages:
        path , version = pId.getPackageInfo()
        CraftCore.log.info(f"{path}: {filename}")
