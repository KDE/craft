import info
import shells


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20160719"
        # don't set an actual version  instead of base. Msys must be manually updated so doing a craft update of msys wil break things.
        if compiler.isX86():
            self.targets[ "base" ] = "http://downloads.sourceforge.net/sourceforge/msys2/msys2-base-i686-%s.tar.xz" % ver
        else:
            self.targets[ "base" ] = "http://downloads.sourceforge.net/sourceforge/msys2/msys2-base-x86_64-%s.tar.xz" % ver
            self.targetDigests['base'] = (['a3255ebba5888c3b4de7a01b6febce9336c66128953f061f7d80e1d8c56582ca'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "base"


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True
        self.shell = shells.MSysShell()

    def install( self ):
        if compiler.isX64():
           utils.copyDir(os.path.join( self.sourceDir(), "msys64"), os.path.join( self.installDir(), "msys"))
        else:
           utils.copyDir(os.path.join( self.sourceDir(), "msys32"), os.path.join( self.installDir(), "msys"))
        os.makedirs(os.path.join(self.installDir(),"dev-utils","bin"))
        utils.createBat(os.path.join(self.installDir(),"dev-utils","bin","msys.bat"),"python %KDEROOT%\\craft\\bin\\shells.py")
        return True
    
    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
           return False
        msysDir = os.path.join(CraftStandardDirs.craftRoot(),"msys")
        return ( self.shell.execute(".", "echo Firstrun") and #start and restart msys before first use
            utils.system("autorebase.bat", cwd = msysDir) and
                 self.shell.execute(".", "pacman -Syu --noconfirm --force") and
            utils.system("autorebase.bat", cwd = msysDir) and
                 self.shell.execute(".", "pacman -Sy --noconfirm --force") and
                 self.shell.execute(".", "pacman -S base-devel --noconfirm --force --needed") and
            utils.system("autorebase.bat", cwd = msysDir) )
