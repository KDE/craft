# 
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

import os;
import utils;
import re;
import sys;

def toNodeName(file):
    """convert filename to dot node name"""
    return file.replace('\\','').replace('-','').replace('.','').replace(':','').replace('/','').replace('+','')

def toNodeLabel(file,baseDir=None):
    """convert filename to dot node label"""
    if baseDir:
        s = file.replace(baseDir,'')
    else:
        s = file
    if s.find('\\CMakeLists.txt') > -1:
        s = s.replace('\\CMakeLists.txt','')
    
    s = s.replace('.\\','').replace('\\','\\\\')
  
    if s.startswith('\\'):
        return s[2:]

    if len(s) < 1:
        return "toplevel"
    return s;

class CMakeDependencies:
    def __init__(self):
        self.files1 = []
        self.files2 = []
        self.packageIncludes = dict() # where a package is included 
        self.packageUsage = dict()    # where package related variables are used (search string=xxx_INCLUDE or xxx_LIBRAR)
        
    def parse(self,dir):
        """find CMakeLists.txt and parse it"""
        if not os.path.exists(dir):
            return False
        list = utils.findFiles(dir,"CMakelists.txt")
        for file in list:
            f = open(file,"r")
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                if line.lower().find("find_package") > -1:
                    m = re.search(r"\(([a-zA-Z0-9]+)[ \)]", line.upper())
                    if m:
                        if not file in self.files1:
                            self.files1.append(file)
                        key = m.groups()
                        if key in self.packageIncludes:
                            if not file in self.packageIncludes[key]:
                                self.packageIncludes[key].append(file)
                        else:
                            self.packageIncludes[key] = [file]
                            
        # find package usage
        for file in list:
            f = open(file,"r")
            for _line in f.readlines():
                line = _line.upper()
                if line.startswith("#"):
                    continue
                for key in self.packageIncludes: 
                    keyInclude = "%s_INCLUDE" % key
                    keyLib = "%s_LIBRAR" % key
                    keyExec = "%s_EXEC" % key
                    if line.find(keyInclude) > -1 or line.find(keyLib) > -1 or line.find(keyExec) > -1:
                        if not file in self.files2:
                            self.files2.append(file)
                        if key in self.packageUsage:
                            if not file in self.packageUsage[key]:
                                self.packageUsage[key].append(file)
                        else:
                            self.packageUsage[key] = [file]
        return True

    def toDot(self,title="",baseDir=None,outFile=None):
        """dump out internal structure as dot file"""
        if outFile <> None: 
            sys.stdout = open(outFile,"w")
            # check if valid
            
        print "digraph G {"
        print "rankdir=LR;"
        print "title [label=\"%s\" color=lightgrey shape=record];" % title
        
        print "subgraph legend {"
        print "A [Label=\"\"];"
        print "B [Label=\"\" shape=record];"
        print "C [Label=\"\"];"
        print "A -> B [color=green,label=\"directory A includes cmake package B\"];"
        print "B -> C [label=\"directory C uses variables provided by cmake package B\"];"
        print "}"
        

        print "{ rank=same; "
        for file in self.files1: 
            print "%s_include [label=\"%s\"];" % (toNodeName(file),toNodeLabel(file,baseDir))
        print "}"

        print "{ rank=same; "
        for file in self.files2: 
            print "%s_uses [label=\"%s\"];" % (toNodeName(file),toNodeLabel(file,baseDir))
        print "}"

        print "{ rank=same; "
        for node in self.packageIncludes: 
            print "%s [shape=record];" % (node[0])
        print "}"

        for node in self.packageIncludes: 
            #print "%s;" % (node[0])
            for file in self.packageIncludes[node]: 
                print "%s_include -> %s [color=green];" % (toNodeName(file),node[0])

        for key in self.packageUsage: 
            for value in self.packageUsage[key]: 
                print "%s -> %s_uses ;" % (key[0],toNodeName(value))
        print "}"

        if outFile <> None:
            sys.stdout=sys.__stdout__   
        return True
    

if __name__ == '__main__':
    dir = sys.argv[1]
    a = CMakeDependencies()
    a.parse(dir)
    title = ''
    if sys.argc >= 3:
        title = sys.argv[2]
    baseDir = None
    if sys.argc >=4:
        baseDir = sys.argv[3]
    outFile = None
    if sys.argc >= 5:
        outFile = sys.argv[4]
        
    a.toDot(title,baseDir,outFile)
