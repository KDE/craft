import utils
from EmergeConfig import *
import InstallDB

def backup():
    utils.copyFile(os.path.join( EmergeStandardDirs.etcPortageDir(), "install.db"), os.path.join( EmergeStandardDirs.etcPortageDir(), "install.db.backup"),linkOnly=False)
    utils.copyFile(os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini"), os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini.backup"),linkOnly=False)

def restore():
    utils.moveFile(os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini.backup"), os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini"))
    utils.moveFile(os.path.join( EmergeStandardDirs.etcPortageDir(), "install.db.backup"), os.path.join( EmergeStandardDirs.etcPortageDir(), "install.db"))

def removeFromDB(category):
    db = InstallDB.InstallDB()
    list = db.getDistinctInstalled(category)
    for c,p,_ in list:
        for package in db.getInstalledPackages( c, p ):
            package.uninstall()

if __name__ == "__main__":
    utils.setVerbose(3)
    # we don't use the db directly and the file must not be locked
    del InstallDB.installdb
    backup()
    removeFromDB("dev-util")
    removeFromDB("gnuwin32")
    with open( os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini.backup"),"rt+") as fin:
        text = fin.read()
        reg = re.compile("^PACKAGE_IGNORES.*$", re.MULTILINE)
        text = reg.sub("PACKAGE_IGNORES =",text)
        with open( os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini"),"wt+") as fout:
            fout.write(text)
    utils.createDir(EmergeStandardDirs.tmpDir())
    archiveName = os.path.join(EmergeStandardDirs.tmpDir(), "framewroks-sdk.7z")
    utils.deleteFile(archiveName)
    utils.system("7za  a %s %s -x!build -x!msys -x!dev-utils -x!tmp -x!mingw* -x!etc/kdesettings.ini.backup -x!etc/portage/install.db.backup" % ( archiveName, EmergeStandardDirs.emergeRoot()))
    restore()