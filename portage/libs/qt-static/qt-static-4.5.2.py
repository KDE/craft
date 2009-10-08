# -*- coding: utf-8 -*-
import utils
import info

#
# static qt package for kdewin installer. The installer expects a static qt library 
# with static runtime (-MT linker flag). This requires a patch in 
# mkspecs\win32-msvc2008\qmake.conf for msvc-2008. 
# 

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.4.3-3'] = 'branches/qt/4.4'
        self.svnTargets['4.5.1-1'] = 'trunk/qt-copy/'
        self.svnTargets['static'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|v4.5.2"
        self.svnTargets['master'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git"
        self.svnTargets['4.5.2-patched'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|v4.5.2"
        self.defaultTarget = '4.5.2-patched'
        self.options.package.packageName = 'qt'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'

from Package.QMakePackageBase import *

class Package(QMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__(self)
        self.subinfo.options.make.makeOptions = "sub-winmain sub-tools-bootstrap sub-moc sub-rcc sub-uic sub-corelib sub-gui"

    def unpack( self ):
        if not QMakePackageBase.unpack(self):
            return False
        utils.applyPatch( self.sourceDir(), os.path.join(self.packageDir(),"qconf.patch"), 1)
        return True
        
    def configure( self ):
        platform = ""
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            platform = "win32-%s" % self.compiler()
        elif self.compiler() == "mingw":
            platform = "win32-g++"
        else:
            exit( 1 )

        incdirs=""
        libdirs=""
        os.environ[ "USERIN" ] = "y"
        userin = "y"
        
        configureTool = r"echo %s | %s " %  \
            (userin, os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" ) )
            
        configureOptions = ""
        if self.buildType() == "Debug":
            configureOptions += " -debug "
        else:
            configureOptions += " -release "

        configureOptions += "-opensource -platform %s -prefix %s -static " \
          " -qt-gif -qt-libpng -no-libjpeg -no-libtiff" \
          " -no-phonon -no-qdbus -no-qt3support -no-webkit -no-scripttools -no-openssl " \
          " -no-opengl -no-xmlpatterns -no-exceptions -no-rtti -no-stl -no-accessibility" \
          " -no-vcproj -no-dsp -no-sql-sqlite" \
          " -no-style-cde -no-style-cleanlooks -no-style-motif -no-style-plastique" \
          " -nomake demos -nomake examples -nomake docs" \
          "%s %s" % (  platform, self.installDir(), incdirs, libdirs)
          
        return QMakePackageBase.configure(self, configureTool, configureOptions)

    def install( self ):
        targets = 'install_qmake install_mkspecs'
        for target in ['winmain', 'uic', 'moc', 'rcc', 'corelib', 'gui', 'xml']:
            targets += ' sub-%s-install_subtargets' % target
         
        if not QMakePackageBase.install(self, targets):
            return False

        # create qt.conf 
        utils.copyFile( os.path.join( self.packageDir(), "qt.conf" ), os.path.join( self.installDir(), "bin", "qt.conf" ) )
        
        # at least in qt 4.5.2 the default mkspecs is not installed which let qmake fail with "QMAKESPEC has not been set, so configuration cannot be deduced."
        default_mkspec = os.path.join(self.installDir(), "mkspecs", "default")
        if not os.path.exists(default_mkspec): 
            utils.copySrcDirToDestDir( os.path.join(self.buildDir(), "mkspecs", "default"), default_mkspec )
        
        # install msvc debug files if available
        if self.buildType() == "Debug" and (self.compiler() == "msvc2005" or self.compiler() == "msvc2008"):
            srcdir = os.path.join( self.buildDir(), "lib" )
            destdir = os.path.join( self.installDir(), "lib" )

            filelist = os.listdir( srcdir )
            
            for file in filelist:
                if file.endswith( ".pdb" ):
                    utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )
                
        return True

    def qmerge( self ):
        utils.debug("this package is not intended to be merged");
        return True

if __name__ == '__main__':
    Package().execute()
