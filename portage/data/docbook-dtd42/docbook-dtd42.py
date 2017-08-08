import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

    def setTargets(self):
        for ver in ['4.2', '4.5']:
            self.targets[ver] = 'http://www.docbook.org/xml/' + ver + '/docbook-xml-' + ver + '.zip'
            self.targetInstallPath[ver] = 'share/xml/docbook/schema/dtd/%s' % ver
        for ver in ['5.0']:
            self.targets[ver] = 'http://www.docbook.org/xml/' + ver + '/docbook-' + ver + '.zip'
            self.targetInstallPath[ver] = 'share/xml/docbook/schema/dtd/%s' % ver
        self.targetDigests['4.2'] = '5e3a35663cd028c5c5fbb959c3858fec2d7f8b9e'
        self.targetDigests['4.5'] = 'b9124233b50668fb508773aa2b3ebc631d7c1620'
        self.targetDigests['5.0'] = '49f274e67efdee771300cba4da1f3e4bc00be1ec'

        self.description = "document type definition for docbook format"
        # note: use the version specified as DOCBOOKXML_CURRENTDTD_VERSION in
        #       FindDocBookXML.cmake of kdelibs or install all DTDs at the same time 
        self.defaultTarget = '4.2'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
