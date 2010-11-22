/* This file is part of the KDE project
   Copyright (C) 2003-2004 Jaroslaw Staniek <staniek@kde.org>

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU Library General Public
   License as published by the Free Software Foundation; either
   version 2 of the License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Library General Public License for more details.

   You should have received a copy of the GNU Library General Public License
   along with this program; see the file COPYING.  If not, write to
   the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.
*/

#ifndef SMI_UNISTD_H
#define SMI_UNISTD_H

#define environ _environ

#ifdef __cplusplus
extern "C" {
#endif

extern int optind;

#define	F_OK	0
#define	R_OK	4
#define	W_OK	2
#define	X_OK	1 

#ifndef STDIN_FILENO
#define STDIN_FILENO 0
#endif

#ifndef STDOUT_FILENO
#define STDOUT_FILENO 1
#endif

#ifndef STDERR_FILENO
#define STDERR_FILENO 2
#endif

#if _MSC_VER < 1600
#define ENOTSUP       ENOSYS
#endif
// from sys/types.h:
#ifndef __MINGW32__
typedef int mode_t;
#endif
typedef unsigned int gid_t;
typedef unsigned int uid_t;
typedef int pid_t;
#ifdef __cplusplus
}
#endif

#endif // KDEWIN_UNISTD_H
