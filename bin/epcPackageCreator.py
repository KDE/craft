import json
import sys
import utils
import os
from time import strftime
        
class EpcPackageCreator(object):     
        def __init__( self , epcFile ):
            self.epcFile = epcFile
            self.epcDict = dict()
            self.variables = dict()
            self.kderoot = os.getenv("KDEROOT")
            self.template = None
            self.versions = list()
            self.default_target = None
            self.build_dependencies = list()
            self.packages = list()
            self.prefix = ""
            self.packagebase = "CMakePackageBase"
            self.portageDir = ""
            
            
            
        def parse(self):
          print(self.epcFile)
          json_file = open(self.epcFile)
          tmp = json.load(json_file)
          self.epcDict = tmp["epc"]
          self.variables = tmp["vars"]
          self.template = str(self.epcDict["template"])
          self.versions = str(self.epcDict["versions"])
          self.default_target = str(self.epcDict["default-target"])
          self.build_dependencies = self.epcDict["buildtime-dependencies"]
          self.packages = self.epcDict["packages"]
          self.prefix = str(self.epcDict["prefix"])
          self.packagebase = str(self.epcDict["package-base"])
          self.portageDir = str(self.epcDict["portage-dir"])
          
          
        def generateSubModule(self):            
            for package in self.packages:
                text = self.template
                for key in self.epcDict.keys():
                  text = text.replace("${EPC_%s}" % key.upper(), str(self.epcDict[key]))
                text = text.replace("${EPC_PACKAGE-NAME}" , package)
                for key in self.variables.keys():
                  text = text.replace("${%s}" % variables.uppercase() , str(self.epcDict[variables]))
                  
                dependencies = "    def setDependencies( self ):\n"
                for dep in self.build_dependencies:
                    dependencies += "        self.buildDependencies['%s'] = 'default'\n" % dep
    
                self.createPackage("%s\n\n%s\n%s" % (text ,dependencies, self._getPpackageText(self.packagebase)),"%s-%s" % (self.prefix, package),os.path.join(self.kderoot,"emerge","portage",self.portageDir,"%s-%s" % (self.prefix,package)))
                

        def generateBaseModule(self):            
            text = "import info\n\nclass subinfo(info.infoclass):\n    def setTargets( self ):\n        self.svnTargets['%s'] = ''\n        self.defaultTarget = '%s'\n\n    def setDependencies( self ):\n" % (self.default_target ,self.default_target )
            for package in self.packages:
                text += "        self.dependencies['%s-%s'] = 'default'\n" % (self.portageDir,package)                
            text +=self._getPpackageText("VirtualPackageBase")                
            self.createPackage(text,self.prefix,os.path.join(self.kderoot,"emerge","portage",self.portageDir))

                
        def createPackage(self,text,name,dest):
                if not os.path.exists(dest):
                   os.makedirs(dest)
                else:
                   for old in os.listdir(dest):
                      if old.endswith(".py"):
                        os.remove(os.path.join(dest,old))
                out = open(os.path.join(dest,"%s-%s-%s.py" % (name,self.default_target,strftime("%Y%m%d"))),"wt+")
                out.write(text)
                print(text)
        
          
        def _getPpackageText(self,packageBase):
           return "\nfrom Package.%s import *\n\nclass Package( %s ):\n    def __init__( self ):\n        self.subinfo = subinfo()\n        %s.__init__( self )\n\n\nif __name__ == '__main__':\n    Package().execute()\n" % (packageBase,packageBase,packageBase)

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        utils.die("")
        
    executableName = sys.argv.pop( 0 )
    epc = EpcPackageCreator(sys.argv.pop(0))
    epc.parse()
    epc.generateSubModule()
    epc.generateBaseModule()