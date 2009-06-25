# -*- coding: utf-8 -*-
import base
import os
import info

class subinfo(info.infoclass):
    def info( self ):
        self.infotext = """What is OpenJPEG?

The OpenJPEG library is an open-source JPEG 2000 codec written in C language. It
has been developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG). In
addition to the basic codec, various other features are under development, among
them the JP2 and MJ2 (Motion JPEG 2000) file formats, an indexing tool useful
for the JPIP protocol, JPWL-tools for error-resilience, a Java-viewer for
j2k-images, ... """

        self.url = """http://www.openjpeg.org/"""
        self.purpose = """openjpeg library can be used in poppler to display OpenJPEG images"""

    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.3']:
            self.targets[ version ] = repoUrl + "/OpenJPEG-" + version + "-bin.tar.bz2 " +\
                                      repoUrl + "/OpenJPEG-" + version + "-lib.tar.bz2"

            
        self.defaultTarget = '1.3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
