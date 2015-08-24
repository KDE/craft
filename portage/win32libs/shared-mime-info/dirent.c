/* ====================================================================
 * The Apache Software License, Version 1.1
 *
 * Copyright (c) 2000-2002 The Apache Software Foundation.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * 3. The end-user documentation included with the redistribution,
 *    if any, must include the following acknowledgment:
 *       "This product includes software developed by the
 *        Apache Software Foundation (http://www.apache.org/)."
 *    Alternately, this acknowledgment may appear in the software itself,
 *    if and wherever such third-party acknowledgments normally appear.
 *
 * 4. The names "Apache" and "Apache Software Foundation" must
 *    not be used to endorse or promote products derived from this
 *    software without prior written permission. For written
 *    permission, please contact apache@apache.org.
 *
 * 5. Products derived from this software may not be called "Apache",
 *    nor may "Apache" appear in their name, without prior written
 *    permission of the Apache Software Foundation.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED.  IN NO EVENT SHALL THE APACHE SOFTWARE FOUNDATION OR
 * ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 * USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 * ====================================================================
 *
 * This software consists of voluntary contributions made by many
 * individuals on behalf of the Apache Software Foundation.  For more
 * information on the Apache Software Foundation, please see
 * <http://www.apache.org/>.
 *
 * Portions of this software are based upon public domain software
 * originally written at the National Center for Supercomputing Applications,
 * University of Illinois, Urbana-Champaign.
 */

#include <windows.h>

#include <malloc.h>
#include <string.h>
#include <errno.h>

#include "dirent.h"

/**********************************************************************
 * Implement dirent-style opendir/readdir/closedir on Window 95/NT
 *
 * Functions defined are opendir(), readdir() and closedir() with the
 * same prototypes as the normal dirent.h implementation.
 *
 * Does not implement telldir(), seekdir(), rewinddir() or scandir(). 
 * The dirent struct is compatible with Unix, except that d_ino is 
 * always 1 and d_off is made up as we go along.
 *
 * The DIR typedef is not compatible with Unix.
 **********************************************************************/

#ifndef __MINGW32__

#ifdef _WIN32_WCE
/* Wrap ASCII functions to UNICODE */

static BOOL
convert_find_data (LPWIN32_FIND_DATAW fdw, LPWIN32_FIND_DATAA fda)
{
    char *filename;
    int len;

    fda->dwFileAttributes = fdw->dwFileAttributes;
    fda->ftCreationTime = fdw->ftCreationTime;
    fda->ftLastAccessTime = fdw->ftLastAccessTime;
    fda->ftLastWriteTime = fdw->ftLastWriteTime;
    fda->nFileSizeHigh = fdw->nFileSizeHigh;
    fda->nFileSizeLow = fdw->nFileSizeLow;

    filename = strWtoA (fdw->cFileName);
    if (!filename)
        return FALSE;

    len = sizeof (fda->cFileName);
    strncpy (fda->cFileName, filename, len);
    fda->cFileName[len - 1] = '\0';

    return TRUE;
}

static LPWSTR
strAtoW( LPCSTR str )
{
    LPWSTR ret = NULL;
    if (str)
    {
        DWORD len = MultiByteToWideChar( CP_ACP, 0, str, -1, NULL, 0 );
        if ((ret = ( WCHAR* )malloc( len * sizeof(WCHAR) )))
            MultiByteToWideChar( CP_ACP, 0, str, -1, ret, len );
    }
    return ret;
}

static LPSTR
strWtoA( LPCWSTR str )
{
    LPSTR ret = NULL;
    if (str)
    {
        DWORD len = WideCharToMultiByte( CP_ACP, 0, str, -1, NULL, 0, NULL, NULL );
        if ((ret = ( char* )malloc( len )))
            WideCharToMultiByte( CP_ACP, 0, str, -1, ret, len, NULL, NULL );
    }
    return ret;
}

HANDLE
FindFirstFileA (LPCSTR lpFileName, LPWIN32_FIND_DATAA lpFindFileData)
{
    wchar_t *pathname;
    WIN32_FIND_DATAW find_file_data;
    HANDLE result;
    int err;

    pathname = strAtoW (lpFileName);
    if (!pathname)
        return INVALID_HANDLE_VALUE;

    result = FindFirstFileW (pathname, &find_file_data);
    if (result != INVALID_HANDLE_VALUE)
    {
        BOOL res = convert_find_data (&find_file_data, lpFindFileData);
        if (! res)
        {
            err = GetLastError ();
            FindClose (result);
            SetLastError (err);
            result = INVALID_HANDLE_VALUE;
        }
    }

    err = GetLastError ();
    free (pathname);
    SetLastError (err);
    return result;
}

    BOOL
FindNextFileA (HANDLE hFindFile, LPWIN32_FIND_DATAA lpFindFileData)
{
    WIN32_FIND_DATAW find_file_data;
    BOOL result;
    int err;

    result = FindNextFileW (hFindFile, &find_file_data);
    if (result)
        result = convert_find_data (&find_file_data, lpFindFileData);

    return result;
}
#endif

KDEWIN_EXPORT DIR * opendir(const char *dir)
{
    DIR *dp;
    char *filespec;
    HANDLE handle;
    int index;

    filespec = (char * )malloc(strlen(dir) + 2 + 1);
    strcpy(filespec, dir);
    index = strlen(filespec) - 1;
    if (index >= 0 && (filespec[index] == '/' || filespec[index] == '\\'))
        filespec[index] = '\0';
    strcat(filespec, "\\*");

    dp = (DIR *)malloc(sizeof(DIR));
    dp->offset = 0;
    dp->finished = 0;
    dp->dir = strdup(dir);

    handle = FindFirstFileA(filespec, &(dp->fileinfo));
    if (handle == INVALID_HANDLE_VALUE)
    {
        if (GetLastError() == ERROR_NO_MORE_FILES) {
            dp->finished = 1;
        }
        else
            return NULL;
    }

    dp->handle = handle;
    free(filespec);
    return dp;
}

KDEWIN_EXPORT struct dirent * readdir(DIR *dp)
{
    int saved_err = GetLastError();

    if (!dp || dp->finished)
        return NULL;

    if (dp->offset != 0)
    {
        if (FindNextFileA(dp->handle, &(dp->fileinfo)) == 0)
        {
            if (GetLastError() == ERROR_NO_MORE_FILES)
            {
                SetLastError(saved_err);
                dp->finished = 1;
            }
            return NULL;
        }
    }
    dp->offset++;

    strncpy(dp->dent.d_name, dp->fileinfo.cFileName, _MAX_FNAME);
    dp->dent.d_ino = 1;
    dp->dent.d_reclen = strlen(dp->dent.d_name);
    dp->dent.d_off = dp->offset;

    return &(dp->dent);
}

KDEWIN_EXPORT int closedir(DIR *dp)
{
    if (!dp)
        return 0;
    FindClose(dp->handle);
    if (dp->dir)
        free(dp->dir);
    if (dp)
        free(dp);

    return 0;
}

#endif /* #ifndef __MINGW32__ */
