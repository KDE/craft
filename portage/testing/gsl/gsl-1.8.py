import base

SRC_URI= """
http://downloads.sourceforge.net/gnuwin32/gsl-1.8-bin.zip
http://downloads.sourceforge.net/gnuwin32/gsl-1.8-lib.zip
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    if self.traditional:
        self.instdestdir = "win32libs"
    else:
        self.instdestdir = ""

if __name__ == '__main__':
    subclass().execute()
