/** 
  emerge configuration wizard 
  
  copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
  
  Licensed under the GPL license, see http://www.gnu.org/licenses/gpl-2.0.txt
  
  This helper tools is intended to be started from the 7z self extractor stub. 
*/ 

#include <windows.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    char path[1024];
  
    if (!GetCurrentDirectory(sizeof(path)-1,path))
        return 1;

    if (!CreateDirectory("etc",NULL))
        return 2;
    
    if (!CopyFile("emerge/kdesettings-example.bat", "etc/kdesettings.bat", TRUE))
        return 3;
    
    CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
    HINSTANCE instance = ShellExecute(NULL, "edit", "etc/kdesettings.bat", NULL, NULL, SW_SHOWNORMAL);
    return instance < (HINSTANCE)32 ? 4 : 0;
}
