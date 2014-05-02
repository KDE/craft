# -*- coding: utf-8 -*-
# Helper script for substitution of paths, independent of cmd or powershell
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

from emerge_config import *
import utils
import subprocess
import argparse

from Source.SourceBase import *
from Source.VersionSystemSourceBase import *
import compiler

def subst( path, drive ):
    if not os.path.exists( path ):
        os.mkdir( path )
    command = "subst %s %s" % ( emergeSettings.get( "ShortPath", drive ), path)
    subprocess.Popen( command, stdout = subprocess.PIPE )

def printBanner():
    print("KDEROOT     : %s" % emergeRoot())
    print("KDECOMPILER : %s" % compiler.getCompilerName() )
    print("KDESVNDIR   : %s" % VersionSystemSourceBase.svnDir())
    print("KDEGITDIR   : %s" % VersionSystemSourceBase.gitDir())
    print("DOWNLOADDIR : %s" % SourceBase.downloadDir())
    print("PYTHONPATH  : %s" % emergeSettings.get("Paths", "PYTHONPATH"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--subst", action = "store_true")
    parser.add_argument("--get", action = "store_true")
    parser.add_argument("--print-banner", action= "store_true")
    parser.add_argument("rest", nargs = argparse.REMAINDER)
    args = parser.parse_args()

    if args.subst:
        if emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH", False ):
            subst( os.path.abspath( os.path.join( os.path.dirname( sys.argv[ 0 ] ), "..", ".." ) ), "EMERGE_ROOT_DRIVE" )
            subst( emergeSettings.get( "Paths", "DOWNLOADDIR" ), "EMERGE_DOWNLOAD_DRIVE" )
            subst( emergeSettings.get( "Paths", "KDESVNDIR" ), "EMERGE_SVN_DRIVE" )
            subst( emergeSettings.get( "Paths", "KDEGITDIR" ), "EMERGE_GIT_DRIVE" )
            print( emergeSettings.get( "ShortPath", "EMERGE_ROOT_DRIVE" ) )
        else:
            print( emergeRoot( ) )
    elif args.get:
        default = ""
        if len(args.rest) == 3:
            default = args.rest[2]
        print(emergeSettings.get(args.rest[0],args.rest[1],default))
    elif args.print_banner:
        printBanner()

