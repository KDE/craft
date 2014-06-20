import portage
import re
import utils
import InstallDB

def printSearch(search_category, search_package,maxDist = 2):
        installable = portage.PortageInstance.getInstallables()
        similar = []
        match = None
        package_re = re.compile(".*%s.*" % search_package.lower())
        for category,package,version in installable:
            if search_category == "" or search_category == category:
                meta = portage.PortageInstance.getMetaData( category, package, version )
                levDist = utils.levenshtein(search_package.lower(),package.lower())
                if levDist == 0 :
                    match = (levDist,category,package,version,meta)
                    break;
                elif package_re.match(package.lower()):
                    similar.append((levDist-maxDist,category,package,version,meta))
                elif len(package)>maxDist and levDist <= maxDist:
                    similar.append((levDist,category,package,version,meta))
                else:
                    if "shortDescription" in meta:
                        if package_re.match(meta["shortDescription"].lower()):                        
                            similar.append((100,category,package,version,meta))
                
        if match == None:
            if len(similar)>0:
                print("Emerge was unable to find %s, similar packages are:" % search_package) 
                similar.sort()
            else:
                print("Emerge was unable to find %s" % search_package)
        else:
            print("Package %s found:" % search_package)
            similar = [match]
        
        for levDist,category,package,version,meta in similar:
            utils.debug((category,package,version,levDist),1)
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
    