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
    list = InstallDB.installdb.getDistinctInstalled(category)
    for c,p,_ in list:
        for package in InstallDB.installdb.getInstalledPackages( c, p ):
            package.uninstall()

if __name__ == "__main__":
    utils.setVerbose(3)
    backup()
    removeFromDB("dev-util")
    with open( os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini.backup"),"rt+") as fin:
        text = fin.read()
        reg = re.compile("^PACKAGE_IGNORES.*$", re.MULTILINE)
        text = reg.sub("PACKAGE_IGNORES =",text)
        with open( os.path.join( EmergeStandardDirs.etcDir(), "kdesettings.ini"),"wt+") as fout:
            fout.write(text)
    utils.createDir(EmergeStandardDirs.tmpDir())
    utils.system("7za  a %s/framewroks-sdk.7z %s -x!build -x!msys -x!dev-utils -x!tmp -x!mingw* -x!etc/kdesettings.ini.backup -x!etc/portage/install.db.backup" % ( EmergeStandardDirs.tmpDir(), EmergeStandardDirs.emergeRoot()))
    restore()