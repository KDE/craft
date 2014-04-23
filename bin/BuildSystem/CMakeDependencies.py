#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

import os
import re
import sys

import utils


def toNodeName(fileName):
    """convert filename to dot node name"""
    return fileName.replace('\\','').replace('-','').replace('.','').replace(':','').replace('/','').replace('+','')

def toNodeLabel(fileName, baseDir=None):
    """convert filename to dot node label"""
    if baseDir:
        s = fileName.replace(baseDir,'')
    # TODO: we can simply say fileName = fileName.replace() and remove the else clause
    else:
        s = fileName
    if s.find('\\CMakeLists.txt') > -1: # TODO: this find is superfluous
        s = s.replace('\\CMakeLists.txt','')

    s = s.replace('.\\','').replace('\\','\\\\')

    if s.startswith('\\'):
        return s[2:]

    if len(s) < 1:
        return "toplevel"
    return s

class CMakeDependencies(object):
    def __init__(self):
        self.files1 = []
        self.files2 = []
        self.packageIncludes = dict() # where a package is included
        self.packageUsage = dict()    # where package related variables are used (search string=xxx_INCLUDE or xxx_LIBRAR)

    def parse(self, directory):
        """find CMakeLists.txt and parse it"""
        if not os.path.exists(directory):
            return False
        fileNames = utils.findFiles(directory, "CMakelists.txt")
        for fileName in fileNames:
            with open(fileName, "r") as f:
                for line in f.readlines():
                    if line.startswith("#"):
                        continue
                    if line.lower().find("find_package") > -1:
                        m = re.search(r"\(([a-zA-Z0-9]+)[ \)]", line.upper())
                        if m:
                            if not fileName in self.files1:
                                self.files1.append(fileName)
                            key = m.groups()
                            if key in self.packageIncludes:
                                if not fileName in self.packageIncludes[key]:
                                    self.packageIncludes[key].append(fileName)
                            else:
                                self.packageIncludes[key] = [fileName]

        # find package usage
        for fileName in fileNames:
            with open(fileName, "r") as f:
                for _line in f.readlines():
                    line = _line.upper()
                    if line.startswith("#"):
                        continue
                    for key in self.packageIncludes:
                        keyInclude = "%s_INCLUDE" % key
                        keyLib = "%s_LIBRAR" % key
                        keyExec = "%s_EXEC" % key
                        if line.find(keyInclude) > -1 or line.find(keyLib) > -1 or line.find(keyExec) > -1:
                            if not fileName in self.files2:
                                self.files2.append(fileName)
                            if key in self.packageUsage:
                                if not fileName in self.packageUsage[key]:
                                    self.packageUsage[key].append(fileName)
                            else:
                                self.packageUsage[key] = [fileName]
        return True

    def toDot(self, title="", baseDir=None, outFile=None):
        """dump out internal structure as dot file"""
        if outFile != None:
            sys.stdout = open(outFile, "w")
            # check if valid

        print("digraph G {")
        print("rankdir=LR;")
        print("title [label=\"%s\" color=lightgrey shape=record];" % title)

        print("subgraph legend {")
        print("A [Label=\"\"];")
        print("B [Label=\"\" shape=record];")
        print("C [Label=\"\"];")
        print("A -> B [color=green, label=\"directory A includes cmake package B\"];")
        print("B -> C [label=\"directory C uses variables provided by cmake package B\"];")
        print("}")


        print("{ rank=same; ")
        for fileName in self.files1:
            print("%s_include [label=\"%s\"];" % (toNodeName(fileName), toNodeLabel(fileName, baseDir)))
        print("}")

        print("{ rank=same; ")
        for fileName in self.files2:
            print("%s_uses [label=\"%s\"];" % (toNodeName(fileName), toNodeLabel(fileName, baseDir)))
        print("}")

        print("{ rank=same; ")
        for node in self.packageIncludes:
            print("%s [shape=record];" % (node[0]))
        print("}")

        for node in self.packageIncludes:
            #print "%s;" % (node[0])
            for fileName in self.packageIncludes[node]:
                print("%s_include -> %s [color=green];" % (toNodeName(fileName), node[0]))

        for key in self.packageUsage:
            for value in self.packageUsage[key]:
                print("%s -> %s_uses ;" % (key[0], toNodeName(value)))
        print("}")

        if outFile != None:
            sys.stdout = sys.__stdout__
        return True

    def toPackageList(self, title="", baseDir=None, outFile=None):
        """dump out internal structure as dot file"""
        if outFile != None:
            sys.stdout = open(outFile, "w")
            # check if valid

        for node in self.packageIncludes:
            print(node[0])

        if outFile != None:
            sys.stdout = sys.__stdout__
        return True

def main():
    directory = sys.argv[1]
    a = CMakeDependencies()
    a.parse(directory)
    title = ''
    argc = len(sys.argv)
    if argc >= 3:
        title = sys.argv[2]
    baseDir = None
    if argc >= 4:
        baseDir = sys.argv[3]
    outFile = None
    if argc >= 5:
        outFile = sys.argv[4]

    a.toDot(title, baseDir, outFile)

if __name__ == '__main__':
    main()
