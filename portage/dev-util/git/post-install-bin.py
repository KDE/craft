import sys
import os
import subprocess

git = os.path.join(os.getenv("KDEROOT"),"dev-utils","git","bin","git.exe")
print "%s config --global -l" % git
result = subprocess.Popen("%s config --global -l" % git , stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

if not "url.git://anongit.kde.org/.insteadof=kde://" in result:
    subprocess.Popen("%s config --global url.git://anongit.kde.org/.insteadOf kde://" % git,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.Popen("%s config --global url.ssh://git@git.kde.org/.pushInsteadOf kde://" % git,stdout=subprocess.PIPE, stderr=subprocess.PIPE)