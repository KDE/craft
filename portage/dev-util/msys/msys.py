import info
import shells
import io


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20161025"
        arch = "i686"
        if compiler.isX64():
            arch = "x86_64"
        # don't set an actual version  instead of base. Msys must be manually updated so doing a craft update of msys wil break things.
        self.targets[ "base" ] = f"http://repo.msys2.org/distrib/{arch}/msys2-base-{arch}-{ver}.tar.xz"
        self.defaultTarget = "base"


    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
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
        # start and restart msys before first use
        if not self.shell.execute(".", "echo Firstrun") and utils.system("autorebase.bat", cwd = msysDir):
            return False

        def queryForUpdate():
            out = io.BytesIO()
            if not self.shell.execute(".", "pacman -Sy --noconfirm --force"):
                raise Exception()
            self.shell.execute(".", "pacman -Qu --noconfirm", out=out, err=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        try:
            while queryForUpdate():
                if not self.shell.execute(".", "pacman -Su --noconfirm --force") and \
                        utils.system("autorebase.bat", cwd = msysDir):
                    return False
        except Exception as e:
            print(e)
            return False
        return (self.shell.execute(".", "pacman -S base-devel --noconfirm --force --needed") and
            utils.system("autorebase.bat", cwd=msysDir) )