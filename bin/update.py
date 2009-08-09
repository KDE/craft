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
    
    packages = """
astyle
base
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
openssl
perl
pexports
ruby
subversion
wget
upx"""
    for package in packages.split():
        print "removing package %s" % package 
		utils.system("emerge --unmerge %s" % package)	
		# remove all temporary files
		utils.system("emerge --cleanbuild %s" % package)	
	#clean directory 
    utils.cleanDirectory(os.path.join(rootdir,'dev-utils'))
	
    # reinstall packages
    utils.system("emerge --update base")
    done = True
#elif currentVersion == '20090808':
#   add stuff for update   
    
if done:
    f = open( versionFile, "w" )
    f.write(newVersion)
    f.close()
    