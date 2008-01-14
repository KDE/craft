import os
import sys
import shutil

resolutions = ['1024x768', '1280x800', '1280x1024', '1440x900', '1600x1200', '1920x1200']
wallpapers_sourcedir = os.path.join( os.getenv( "KDESVNDIR" ), "trunk", "KDE", "kdebase", "workspace", "wallpapers" )
print "Windows System integration",

if len (sys.argv) > 1:
    if sys.argv[ 1 ] in resolutions or sys.argv[ 1 ].isdigit() and int( sys.argv[ 1 ] ) in range( len( resolutions ) ):
        if sys.argv[ 1 ].isdigit():
            res = resolutions[ int( sys.argv[ 1 ] ) ]
        else:
            res = sys.argv[ 1 ]
        print
        print "*copying Wallpapers*"

        dirlist = os.listdir( wallpapers_sourcedir )
        dirlist.remove('.svn')
        for element in dirlist:
            if os.path.isdir( os.path.join( wallpapers_sourcedir, element ) ):
                print 'copying ' + element.replace('_', ' ') + '.jpg'
                shutil.copy( os.path.join( wallpapers_sourcedir, element, "contents", "images", res + '.jpg' ), 
                             os.path.join( os.getenv( "SYSTEMROOT" ), "Web", "Wallpaper", element.replace('_', ' ') + '.jpg' ) )
                #shutil.move( os.path.join( os.getenv( "SYSTEMROOT" ), "web", "Wallpapers", res + '.jpg' ),
                #             os.path.join( os.getenv( "SYSTEMROOT" ), "web", "Wallpapers",  ))
        exit( 0 )

print "- Help"
print "choose your screen resolution out of the following:"
for element in resolutions:
    print str(resolutions.index(element)) + '\t' + element
print "this script should be understood as a preview, a tighter integration will follow"
