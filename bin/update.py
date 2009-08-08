# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

#
# emerge update script 
# 

import sys
import os
import utils
import portage

rootdir = os.getenv( "KDEROOT" )

newVersion = '20090808'

versionFile = os.path.join(rootdir,'etc','version')
if os.path.exists(versionFile):
    f = open( versionFile, "r" )
    currentVersion = f.read()
    f.close()
else:
    currentVersion = '20090731'

done = False
if currentVersion == '20090731':
    # because the merge destination of some package in the dev-utils category has been changed, 
    # we reinstall all those packages
    
    # delete dev-util packages 1. try 
    path = portage.etcDir()
    fileName = os.path.join(path,'installed')
    if os.path.isfile( fileName ):
        f = open( fileName, "rb" )
        lines = f.read().splitlines()
        f.close()
        for line in lines:
            (_category, _packageVersion) = line.split( "/" )
            (_package, _version) = portage.packageSplit(_packageVersion)
            if _category == 'dev-utils' or _package == 'base':
                print "deleting package %s" % _package
                utils.unmerge( rootdir, _package, True )
                portage.remInstalled(_category, _package, _version)
    # make sure all dev-utils package files are really deleted
    packages = """
astyle
bjam
cmake
doxygen
gettext-tools
git
graphviz
mc
md5sums
mingw
msys
perl
pexports
ruby
subversion
upx"""
    for package in packages.split():
        print package
        utils.unmerge(rootdir,package,True)
    utils.cleanDirectory(os.path.join(rootdir,'dev-util'))
    
    # reinstall packages
    utils.system("emerge --update base")
    done = True
#elif currentVersion == '20090808':
#   add stuff for update   
    
if done:
    f = open( versionFile, "w" )
    f.write(newVersion)
    f.close()
    