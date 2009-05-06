import os
import sys
import subprocess

def die( message ):
    log.write( message )
    print >> sys.stderr, "package.py fatal error: %s" % message
    exit( 1 )

def system( cmdstring, logfile ):
    cmdstring = emerge + " " + cmdstring
    print cmdstring
    #stderr = file( logfile, 'wb' )
    #p = subprocess.Popen( cmdstring, shell=True, stdout=stderr, stderr=stderr )
    p = subprocess.Popen( cmdstring, shell=True )
    ret = p.wait()
    #stderr.close()
    return ( ret == 0 )
  
def kdesupport():
    packages = "qt,4.4.3-3 kdewin-installer,svnHEAD kdewin32,0.3.9 \
                automoc,0.9.88 akonadi,1.1.2 clucene-core,0.9.21-2 \
                eigen2,2.0.1 qca,2.0.1-2 qimageblitz,0.0.5 \
                phonon,4.3.0 soprano,2.2.2 strigi,0.6.5 taglib,1.5.0"
    for d in packages.split():
      (name, version) = d.split(',')
      system( "--unmerge %s" % name, outfile % name )
      if not system( "--install-deps %s" % name, outfile % name ):
        die( "%s FAILED" % full_name )
      if not system( "--target=%s %s" % ( version, name ), outfile % name ):
        die( "%s FAILED\n" % name )
      system( "--package --target=%s %s" % ( version, name ), outfile % name )
      print log.write( "%s OK\n" % name )

def kde_base_system(suffix = ""):
    packages = "kdelibs kdepimlibs kdebase-runtime kdebase-workspace"
    for p in packages.split():
      full_name = "%s/%s" % ( suffix, p )
      system( "--unmerge %s" % p, outfile % p )
      if suffix != "":
        system( "--unmerge %s" % full_name, outfile % p )
      if not system( "--install-deps %s" % full_name, outfile % p ):
        die( "%s FAILED" % full_name )
      if not system( "--offline %s" % full_name, outfile % p ):
        die( "%s FAILED\n" % p )
      if not system( "--package %s" % full_name, outfile % p ):
        die( "%s FAILED" % full_name )
      print log.write( "%s OK\n" % full_name )

def kde_packages(suffix = ""):
    packages = "kdebase-apps kdeedu kdegames kdegraphics kdemultimedia \
                kdenetwork kdesdk kdetoys kdewebdev kdeutils"
    for p in packages.split():
      full_name = "%s/%s" % ( suffix, p )

      system( "--unmerge %s" % p, outfile % p )
      if suffix != "":
        system( "--unmerge %s" % full_name, outfile % p )

      if not system( "--install-deps %s" % full_name, outfile % p ):
        print log.write( "%s FAILED\n" % full_name )
        continue

      if not system( "--offline --full-package %s" % full_name, outfile % p ):
        print log.write( "%s FAILED\n" % full_name )
      else:
        print log.write( "%s OK\n" % full_name )

def kde_languages(suffix = ""):
    p = "l10n-kde4"
    full_name = "%s/%s" % ( suffix, p )
    system( "--unmerge %s" % p, outfile % p )
    if suffix != "":
      system( "--unmerge %s" % full_name, outfile % p )
    if not system( "--install-deps %s" % full_name, outfile % p ):
      print log.write( "%s FAILED\n" % full_name )
      return
    if not system( "--offline --full-package %s" % full_name, outfile % p ):
      print log.write( "%s FAILED\n" % full_name )
    else:
      print log.write( "%s OK\n" % full_name )

os.environ["EMERGE_TARGET"]="4.2.3"
os.environ["EMERGE_OFFLINE"]=""
suffix = "kde-4.2"

logroot = os.path.join( os.environ["KDEROOT"], "emerge", "logs" )

log = file( os.path.join( logroot, "log.txt" ), 'a+' )
outfile = os.path.join( logroot, "log-%s.txt" )
emerge = os.path.join( os.environ["KDEROOT"], "emerge", "bin", "emerge.py" )

log.write( "***************************************\n")
log.write( "START\n")
log.write( "***************************************\n")
kdesupport()
kde_base_system( suffix )
kde_packages( suffix )
kde_languages( suffix )
log.write( "***************************************\n")
log.write( "ENDE\n")
log.write( "***************************************\n")

log.close()
