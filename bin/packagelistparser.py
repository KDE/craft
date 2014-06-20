import utils

class PackageListParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.isParsed = False
        self.packageList = []

    def __parse(self):
        try:
            _listfile = open(self.filename, 'r')
        except:
            utils.error("couldn't open listfile")
            return
        for line in _listfile:
            line = line.strip()
            if line.startswith('#'): continue
            
            _cat, _pac, _target, _patch = line.split(",")
            self.packageList.append((_cat, _pac, _target, _patch))
        self.isParsed = True

    def getFullList( self ):
        if not self.isParsed: self.__parse()
        return self.packageList

    def getPackageList( self ):
        if not self.isParsed: self.__parse()
        return [x[1] for x in self.packageList]

    def getInfoDict( self ):
        if not self.isParsed: self.__parse()
        _d = dict()
        for _cat, _pac, _target, _patch in self.packageList:
            _d[_cat + '/' + _pac] = (_target, _patch)
        return _d

def main():
    parser = PackageListParser("../server/serverconfig/packagelist-win32libs.txt")
    print(parser.getFullList())
    print("\n".join(parser.getPackageList()))
    print(parser.getInfoDict())

if __name__ == '__main__':
    main()
