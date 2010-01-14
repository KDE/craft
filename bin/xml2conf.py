# translate xml file to the 
import sys
import re
import os

if len(sys.argv) < 2:
    print "not enough arguments"
    sys.exit(0)

compilerList = ("mingw", "mingw4", "vc90")

moduleStart = re.compile(r"<module name=\"([^\"]*)\">")
packageStart = re.compile(r"<package name=\"([^\"]*)\"[ ]?(?:comment=.*(meta).*)?>")
packageEnd = re.compile(r"</package>")
dependencyTerm = re.compile(r"<dependency>([^<]*)</dependency>")
descriptionTerm = re.compile(r"<shortDescription>([^<]*)</shortDescription>")

moduleList = dict()
for filename in sys.argv[1:]:
    packageDepsList = dict()
    packageDescriptionList = dict()
    moduleMetaName = ""
    moduleName = ""

    infile = open(filename)
    for line in infile:
        result = moduleStart.search(line)
        if result:
            moduleName = result.group(1)
            for sline in infile:
                result = packageStart.search(sline)
                if result:
                    packageName = result.group(1)
                    if result.group(2) == "meta":
                        moduleMetaName = packageName
                    packageDepsList[packageName] = []
                    for subline in infile:
                        result = dependencyTerm.search(subline)
                        if result:
                            packageDepsList[packageName].append(result.group(1))
                        result = descriptionTerm.search(subline)
                        if result and not packageName == moduleMetaName:
                            packageDescriptionList[packageName] = result.group(1)
                        if packageEnd.search(subline):
                            break
    infile.close()

    # print the header
    print ';'+"-"*55
    print ';', moduleName
    print ';'+"-"*55

    # print the metapackage line
    if moduleMetaName:
        print "@metapackage", moduleMetaName,
        for i in packageDepsList[moduleMetaName]:
            print i,
        print
        packageDepsList.pop(moduleMetaName,"") 
    print ';'

    # print the categorypackages
    for compiler in compilerList:
        print "@categorypackages KDE",
        for package in packageDepsList:
            print package + "-" + compiler,
        print
    print ';'

    # print all dependencies
    for package in packageDepsList:
        for compiler in compilerList:
            print "@deps", package + "-" + compiler, 
            for i in packageDepsList[package]:
                print i + "-" + compiler,
            print
    print ';'
    
    moduleList[moduleName] = packageDescriptionList

print
print ';'+'-'*55
print
for module in moduleList:
    for package in moduleList[module]:
        print "@pkgnotes", package + "-*", moduleList[module][package]

    print
