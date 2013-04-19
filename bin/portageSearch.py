import portage
import re
import utils
import InstallDB

def printSearch(search_category, search_package,maxDist = 3):
        installable = portage.PortageInstance.getInstallables()
        similar = []
        match = None
        package_re = re.compile(".*%s.*" % search_package)
        for category,package,version in installable:
            if search_category == "" or search_category == category:
                levDist = utils.levenshtein(search_package,package)
                if levDist == 0 :
                    match = ((levDist,category,package,version))
                    break;
                elif package_re.match(package):
                    similar.append((levDist-maxDist,category,package,version))
                elif len(package)>maxDist and levDist <= maxDist:
                    similar.append((levDist,category,package,version))
                
        if match == None:
            if len(similar)>0:
                print("Emerge was unable to find %s, similar packages are:" % search_package) 
                similar.sort()
            else:
                print("Emerge was unable to find %s" % search_package)
        else:
            print("Package %s found:" % search_package)
            similar = [match]
        
        for levDist,category,package,version in similar:
            utils.debug((category,package,version,levDist),1)
            meta = portage.PortageInstance.getMetaData( category, package, version )
            description = ""
            if "shortDescription" in meta:
                description = meta["shortDescription"]
            homepage = ""
            if "homepage" in meta:
                homepage = meta["homepage"]
            #print(levDist)
            print("%s/%s" % (category,package))
            print("\t Homepage: %s" % homepage)
            print("\t Description: %s" % description)
            print("\t Latest version: %s" % version)
            print("\t Installed version: %s" % InstallDB.installdb.findInstalled(category,package))
    