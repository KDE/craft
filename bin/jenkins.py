import os
from EmergeConfig import *


def generateJob(package):
    EmergeStandardDirs.allowShortpaths(False)
    path = os.path.join(EmergeStandardDirs.tmpDir(), "jobs", package.package)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "config.xml"), "wt+") as config:
        config.write("""<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description>${DESCRIPTION}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.BatchFile>
      <command>cd ${EMERGE_ROOT} &amp;&amp; ${EMERGE_ROOT}\kdeenv.bat emerge -i ${PACKAGE}
</command>
    </hudson.tasks.BatchFile>
    <hudson.tasks.BatchFile>
      <command>cd ${EMERGE_ROOT} &amp;&amp; ${EMERGE_ROOT}\kdeenv.bat emerge --package ${PACKAGE}</command>
    </hudson.tasks.BatchFile>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>""".replace("${EMERGE_ROOT}", os.path.join(EmergeStandardDirs.emergeRoot(), "emerge").replace("${PACKAGE}",
                                                                                                        package.subinfo.package).replace(
            "${DESCRIPTION}", package.subinfo.shortDescription))
        EmergeStandardDirs.allowShortpaths(True)
        return True
