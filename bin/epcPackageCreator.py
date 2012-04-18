import json
import sys
import utils
import os
import re
from time import strftime

class EpcPackageCreator(object):
    def __init__( self , epcFile ):
        self.epcFile = epcFile        
        self.kderoot = os.getenv("KDEROOT")
        self.epcVariables = re.compile("\$\{.*\}")
        self.epcDict = dict()
        self.variables = dict()
        self.subinfoTemlate = ""
        self.packageTemplate = "from Package.CMakePackageBase import *\n\nclass Package( CMakePackageBase ):\n    def __init__( self ):\n        self.subinfo = subinfo()\n        CMakePackageBase.__init__( self )"
        self.versions = ""
        self.default_target = ""
        self.build_dependencies = list()
        self.dependencies = list()
        self.packages = list()
        self.prefix = ""
        self.suffix = ""
        self.portageDir = ""
        self.description = ""
        self.homepage = ""
        



    def parse(self):
        print(self.epcFile)
        json_file = open(self.epcFile)
        tmp = json.load(json_file)
        self.epcDict = tmp["epc"]
        self.variables = tmp["vars"]
        self.subinfoTemlate = self._get("subinfo-template",self.subinfoTemlate)
        self.packageTemplate = self._get("package-template",self.packageTemplate)
        self.versions = self._get("versions",self.versions)
        self.default_target = self._get("default-target",self.default_target)
        self.build_dependencies = self._get("buildtime-dependencies",self.build_dependencies)        
        self.dependencies = self._get("dependencies" ,self.dependencies)
        self.packages = self._get("packages",self.packages)
        self.prefix = self._get("prefix",self.prefix)
        self.suffix = self._get("suffix",self.suffix )
        self.portageDir = self._get("portage-dir",self.portageDir)
        self.description = self._get("description",self.description)
        self.homepage = self._get("homepage",self.homepage)

    def _get(self,key,target,srcDict = None):
        if srcDict == None:
            srcDict = self.epcDict
        if key in srcDict:
            return type(target)(srcDict[key])
        return target
      
      
    def _getDependencies(self,package):
        text = "\n\n    def setDependencies( self ):\n"
        for dep in self.build_dependencies:
            text += "        self.buildDependencies['%s'] = 'default'\n" % dep
        for dep in self.dependencies:
            text += "        self.dependencies['%s'] = 'default'\n" % dep
        for dep in self._get("buildtime-dependencies",list(),package):
            text += "        self.buildDependencies['%s'] = 'default'\n" % dep
        for dep in self._get("dependencies",list(),package):
            text += "        self.dependencies['%s'] = 'default'\n" % dep
        return text
        
    def _getDigests(self,package):        
        digests = self._get("digests",dict(),package);
        if len(digests) == 0:
            return ""
        text = "\n"
        for key in digests.keys():
            text += "        self.targetDigests['%s'] = '%s'\n" % ( key , digests[key])
        return text
        
    def _getPatches(self,package):
        patches = self._get("patches",dict(),package)
        if len(patches) == 0:
            return ""
        text = ""
        for key in patches.keys():
            patch = patches[key].pop(0)
            text += "\n        self.patchToApply['%s'] = [('%s',%s)" %  (key , patch["patch"],patch["patch-lvl"] )
            for patch in patches[key]:
                print(patch)
                text += "\n                                     ,('%s',%s)" %  ( patch["patch"],patch["patch-lvl"] )
            text += "]"
        text += "\n"
        return text
        
    def _getDescription(self,package):
        text = self._get("description",self.description,package)
        if text == "":
            return ""
        return "\n        self.shortDescription = '%s'\n" % text
        
    def _getHomepage(self,package):
        text = self._get("homepage",self.homepage,package)
        if text == "":
            return ""
        return "\n        self.homepage = '%s'\n" % text
        
        
    def generateSubModule(self):
        for package in self.packages:
            text = self._get("subinfo-template",self.subinfoTemlate,package)
            text += "\n"
            text += self._getDigests(package)
            text += self._getPatches(package)
            text += self._getHomepage(package)
            text += self._getDescription(package)
            text += self._getDependencies(package)

                
            
            text += "\n\n"
            text += self._get("package-template",self.packageTemplate,package)
            text +=  self._getPpackageText()
            
            for key in self.epcVariables.findall(text):
                if key.startswith("${EPC_PACKAGE"):
                    text = text.replace(key, str(package[key[14:-1].lower()]))
                    continue
                if key.startswith("${EPC_"):
                    text = text.replace(key, str(self.epcDict[key[6:-1].lower()]))
                    continue
                text = text.replace(key, str(self.variables[key.lower()]))

            outName = package["name"]
            if self.prefix != "":
              outName = "%s-%s" % (self.prefix,outName)
            if self.suffix != "":
                outName = "%s-%s" % (outName,self.suffix)
  
            dest = os.path.join(self.kderoot,"emerge","portage",self.portageDir,outName)

            self.createPackage(text,outName,dest)


    def generateBaseModule(self):
        text = "import info\n\nclass subinfo(info.infoclass):\n    def setTargets( self ):\n        self.svnTargets['%s'] = ''\n        self.defaultTarget = '%s'\n" % (self.default_target ,self.default_target )
        text += self._getHomepage(self.epcDict)
        text += self._getDescription(self.epcDict)
        text += "\n    def setDependencies( self ):\n"
        pName,module = self.portageDir.split("/")
        for package in self.packages:
            if self.prefix != "":
              name = "%s/%s-%s" % (pName,self.prefix,package["name"])
            else:
              name = "%s/%s" % (pName,package["name"])
            if self.suffix != "":
                name = "%s-%s" % (name,self.suffix)
            text += "        self.dependencies['%s'] = 'default'\n" % name
        text += "\nfrom Package.VirtualPackageBase import *\n\nclass Package( VirtualPackageBase ):\n    def __init__( self ):\n        self.subinfo = subinfo()\n        VirtualPackageBase.__init__( self )"     
        text += self._getPpackageText()            
        self.createPackage(text,module,os.path.join(self.kderoot,"emerge","portage",self.portageDir))


    def createPackage(self,text,name,dest):
        if not os.path.exists(dest):
            os.makedirs(dest)
        else:
            for old in os.listdir(dest):
                if old.endswith(".py"):
                    os.remove(os.path.join(dest,old))
        name = os.path.join(dest,"%s-%s-%s.py" % (name,self.default_target,strftime("%Y%m%d")))
        out = open(name,"wt+")
        out.write(text)
        out.close()
        print(name)
        print(text)


    def _getPpackageText(self,):
        return "\n\n\nif __name__ == '__main__':\n    Package().execute()\n"

if __name__ == '__main__':
    utils.startTimer("EPC")
    if len( sys.argv ) < 2:
        utils.die("")

    executableName = sys.argv.pop( 0 )
    epc = EpcPackageCreator(sys.argv.pop(0))
    epc.parse()
    #print(epc.__dict__)
    epc.generateSubModule()
    epc.generateBaseModule()
    utils.stopTimer("EPC")
