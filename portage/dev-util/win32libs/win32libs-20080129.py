import base
import os
import utils
import shutil
import info

SRC_URI= """
http://82.149.170.66/kde-windows/repository/win32libs/single/aspell-0.60.5-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/aspell-0.60.5-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/boost-headers-1.34-lib.tar.bz2

http://82.149.170.66/kde-windows/repository/win32libs/single/libbzip2-1.0.5-1-bin.tar.bz2
http://82.149.170.66/kde-windows/repository/win32libs/single/libbzip2-1.0.5-1-lib.tar.bz2

http://82.149.170.66/kde-windows/repository/win32libs/single/expat-2.0.1-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/expat-2.0.1-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/giflib-4.1.4-1-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/giflib-4.1.4-1-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/gpgme-1.1.4-3-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/gpgme-1.1.4-3-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/iconv-1.9.2-2-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/iconv-1.9.2-2-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/jasper-1.900.1-2-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/jasper-1.900.1-2-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/jpeg-6.b-5-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/jpeg-6.b-5-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/lcms-1.17-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/lcms-1.17-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/libintl-0.14.4-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/libintl-0.14.4-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/libidn-1.2-1-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/libidn-1.2-1-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/libpng-1.2.23-bin.tar.bz2
http://82.149.170.66/kde-windows/repository/win32libs/single/libpng-1.2.23-lib.tar.bz2

http://82.149.170.66/kde-windows/repository/win32libs/single/libxml2-2.6.30-3-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/libxml2-2.6.30-3-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/libxslt-1.1.22-2-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/libxslt-1.1.22-2-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/openslp-1.2.1-2-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/openslp-1.2.1-2-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/openssl-0.9.8g-1-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/openssl-0.9.8g-1-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/redland-1.0.3-5-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/redland-1.0.3-5-lib.zip

http://download.cegit.de/kde-windows/repository/win32libs/single/shared-mime-info-0.23-bin.tar.bz2

http://82.149.170.66/kde-windows/repository/win32libs/single/tiff-3.8.2-2-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/tiff-3.8.2-2-lib.zip

http://82.149.170.66/kde-windows/repository/win32libs/single/zlib-1.2.3-2-bin.zip
http://82.149.170.66/kde-windows/repository/win32libs/single/zlib-1.2.3-2-lib.zip

http://downloads.sourceforge.net/sourceforge/gnuwin32/zip-2.31-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/zip-2.31-lib.zip
"""

if os.getenv("KDECOMPILER") == "mingw":
    SRC_URI = SRC_URI + """
http://download.cegit.de/kde-windows/repository/win32libs/single/dbus-mingw-1.1.2.20080216-bin.tar.bz2
http://download.cegit.de/kde-windows/repository/win32libs/single/dbus-mingw-1.1.2.20080216-lib.tar.bz2

http://82.149.170.66/kde-windows/repository/win32libs/single/pcre-mingw-7.6-2-bin.tar.bz2
http://82.149.170.66/kde-windows/repository/win32libs/single/pcre-mingw-7.6-2-lib.tar.bz2
"""
else:
    SRC_URI = SRC_URI + """
http://download.cegit.de/kde-windows/repository/win32libs/single/dbus-msvc-1.1.2.20071228-bin.tar.bz2
http://download.cegit.de/kde-windows/repository/win32libs/single/dbus-msvc-1.1.2.20071228-lib.tar.bz2

http://82.149.170.66/kde-windows/repository/win32libs/single/pcre-msvc-7.6-1-bin.tar.bz2
http://82.149.170.66/kde-windows/repository/win32libs/single/pcre-msvc-7.6-1-lib.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['HEAD'] = SRC_URI
        self.defaultTarget = 'HEAD'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    if self.traditional:
        self.instdestdir = "win32libs"
    else:
        self.instdestdir = ""
    self.subinfo = subinfo()

  def compile(self):
    # here we need an own compile step, because we have to copy
    # the boost headers around, so that they are found for kdepimlibs
    srcdir  = os.path.join( self.workdir, "include", "boost-1_34" )
    destdir = os.path.join( self.workdir, "include", "boost-1_34_0" )
    utils.copySrcDirToDestDir( srcdir, destdir )
    if self.compiler == "mingw":
        srcfile = os.path.join( self.workdir, "lib", "libdbus-1.dll.a" )
        destfile = os.path.join( self.workdir, "lib", "libdbus-1d.dll.a" )
        shutil.copy( srcfile, destfile )
        srcfile = os.path.join( self.workdir, "bin", "libdbus-1.dll" )
        destfile = os.path.join( self.workdir, "bin", "libdbus-1d.dll" )
        shutil.copy( srcfile, destfile )

    return True

if __name__ == '__main__':
    subclass().execute()
