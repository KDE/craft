/*
 * rsync-wrapper - replace cwrsync.cmd with an executable
 * based on git-wrapper
 *
 * Copyright (C) 2012 Pat Thoyts <patthoyts@users.sourceforge.net>  (original code)
 * Copyright (C) 2014 Patrick Spendrin <ps_ml@gmx.de>
 */

/*
 * standard msvc commandline: cl /Fersync.exe rsync-wrapper.c /link shlwapi.lib shell32.lib
 */

#define STRICT
#define WIN32_LEAN_AND_MEAN
#define UNICODE
#define _UNICODE
#include <windows.h>
#include <shlwapi.h>
#include <shellapi.h>
#include <stdio.h>

static void
PrintError(LPCWSTR wszPrefix, DWORD dwError)
{
    LPWSTR lpsz = NULL;
    DWORD cch = 0;

    cch = FormatMessageW(FORMAT_MESSAGE_ALLOCATE_BUFFER
                         | FORMAT_MESSAGE_FROM_SYSTEM
                         | FORMAT_MESSAGE_IGNORE_INSERTS,
                         NULL, dwError, LANG_NEUTRAL,
                         (LPTSTR)&lpsz, 0, NULL);
    if (cch < 1) {
        cch = FormatMessageW(FORMAT_MESSAGE_ALLOCATE_BUFFER
                             | FORMAT_MESSAGE_FROM_STRING
                             | FORMAT_MESSAGE_ARGUMENT_ARRAY,
                             L"Code 0x%1!08x!",
                             0, LANG_NEUTRAL, (LPTSTR)&lpsz, 0,
                             (va_list*)&dwError);
    }
    fwprintf(stderr, L"%s: %s", wszPrefix, lpsz);
    LocalFree((HLOCAL)lpsz);
}

int
main(void)
{
    int r = 1, wait = 1;
    WCHAR exepath[MAX_PATH], exe[MAX_PATH];
    LPWSTR cmd = NULL, path2 = NULL, exep = exe;
    UINT codepage = 0;
    int len;

    /* get the installation location */
    GetModuleFileName(NULL, exepath, MAX_PATH);
    PathRemoveFileSpec(exepath);
    PathRemoveFileSpec(exepath);

    /* set the default exe module */
    wcscpy(exe, exepath);
    PathAppend(exe, L"rsync\\bin\\rsync.exe");

    /* set HOME to %HOMEDRIVE%%HOMEPATH% or %USERPROFILE%
     * With roaming profiles: HOMEPATH is the roaming location and
     * USERPROFILE is the local location
     */
    if (GetEnvironmentVariable(L"HOME", NULL, 0) == 0) {
        LPWSTR e = NULL;
        len = GetEnvironmentVariable(L"HOMEPATH", NULL, 0);
        if (len == 0) {
            len = GetEnvironmentVariable(L"USERPROFILE", NULL, 0);
            if (len != 0) {
                e = (LPWSTR)malloc(len * sizeof(WCHAR));
                GetEnvironmentVariable(L"USERPROFILE", e, len);
                SetEnvironmentVariable(L"HOME", e);
                free(e);
            }
        } else {
            int n;
            len += GetEnvironmentVariable(L"HOMEDRIVE", NULL, 0);
            e = (LPWSTR)malloc(sizeof(WCHAR) * (len + 2));
            n = GetEnvironmentVariable(L"HOMEDRIVE", e, len);
            GetEnvironmentVariable(L"HOMEPATH", &e[n], len-n);
            SetEnvironmentVariable(L"HOME", e);
            free(e);
        }
    }

    /* extend the PATH */
    len = GetEnvironmentVariable(L"PATH", NULL, 0);
    len = sizeof(WCHAR) * (len + 2 * MAX_PATH);
    path2 = (LPWSTR)malloc(len);
    wcscpy(path2, exepath);
    PathAppend(path2, L"rsync\\bin;");
    GetEnvironmentVariable(L"PATH", &path2[wcslen(path2)],
                           (len/sizeof(WCHAR))-wcslen(path2));
    SetEnvironmentVariable(L"PATH", path2);
    free(path2);


    /* fix up the command line to call rsync.exe
     */
    {
        int wargc = 0, gui = 0;
        LPWSTR cmdline = NULL;
        LPWSTR *wargv = NULL, p = NULL;
        LPWSTR endOfString = 0;
        cmdline = GetCommandLine();
        wargv = CommandLineToArgvW(cmdline, &wargc);
        cmd = (LPWSTR)malloc(sizeof(WCHAR) * (wcslen(cmdline) + MAX_PATH));
        ZeroMemory(cmd, sizeof(WCHAR)*(wcslen(cmdline) + MAX_PATH));
        wcscpy(cmd, L"rsync.exe");
        endOfString = cmd + wcslen(cmd);
        for(int i = 1; i < wargc; i++) {
            LPWSTR currentPar = NULL;
            WCHAR firstChar = wargv[i][0];
            wcscat(cmd, L" ");
            if(wargv[i][1] == L':' && ((firstChar >= L'A' && firstChar <= L'Z') || (firstChar >= L'a' && firstChar <= L'z'))) {
                wcscat(cmd, L"/cygdrive/");
                if(firstChar >= L'A' && firstChar <= L'Z') {
                    firstChar = L'a' + firstChar - L'A';
                }
                wcsncat(cmd, &firstChar, 1);
                endOfString = cmd + wcslen(cmd);
                wcscat(cmd, &wargv[i][2]);

                for(LPWSTR j = endOfString; j < cmd + wcslen(cmd); j++) {
                    if(*j == L'\\') *j = L'/';
                }
            } else {
                wcscat(cmd, wargv[i]);
            }
        };
        LocalFree(wargv);
    }

    /* set the console to ANSI/GUI codepage */
    codepage = GetConsoleCP();
    SetConsoleCP(GetACP());

    {
        STARTUPINFO si;
        PROCESS_INFORMATION pi;
        BOOL br = FALSE;
        ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));
        ZeroMemory(&si, sizeof(STARTUPINFO));
        si.cb = sizeof(STARTUPINFO);
        br = CreateProcess(exep,/* module: null means use command line */
                           cmd,  /* modified command line */
                           NULL, /* process handle inheritance */
                           NULL, /* thread handle inheritance */
                           TRUE, /* handles inheritable? */
                           CREATE_UNICODE_ENVIRONMENT,
                           NULL, /* environment: use parent */
                           NULL, /* starting directory: use parent */
                           &si, &pi);
        if (br) {
            if (wait)
                WaitForSingleObject(pi.hProcess, INFINITE);
            if (!GetExitCodeProcess(pi.hProcess, (DWORD *)&r))
                PrintError(L"error reading exit code", GetLastError());
            CloseHandle(pi.hProcess);
        } else {
            PrintError(L"error launching rsync", GetLastError());
            r = 1;
        }
    }

    free(cmd);

    /* reset the console codepage */
    SetConsoleCP(codepage);
    ExitProcess(r);
}

/*
 * Local variables:
 * mode: c
 * indent-tabs-mode: nil
 * c-basic-offset: 4
 * tab-width: 4
 * End:
 */
