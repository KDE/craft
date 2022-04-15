; -*- coding: utf-8 -*-
; Copyright (c) 2022 Thomas Friedrichsmeier <thomas.friedrichsmeier@kdemail.net>
;
; Redistribution and use in source and binary forms, with or without
; modification, are permitted provided that the following conditions
; are met:
; 1. Redistributions of source code must retain the above copyright
;    notice, this list of conditions and the following disclaimer.
; 2. Redistributions in binary form must reproduce the above copyright
;    notice, this list of conditions and the following disclaimer in the
;    documentation and/or other materials provided with the distribution.
;
; THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
; ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
; IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
; ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
; FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
; DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
; OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
; HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
; LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
; OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
; SUCH DAMAGE.

[Setup]
AppName=@{productname}
AppVersion=@{version}
WizardStyle=modern
DefaultDirName={autopf}\@{productname}
DefaultGroupName=@{productname}
Compression=lzma2
SolidCompression=yes
; LicenseFile=SomeText.txt or .rtf
@{license}
; InfoBeforeFile=SomeText.txt or .rtf
@{readme}
AppPublisher=@{company}
AppSupportURL=@{website}
PrivilegesRequiredOverridesAllowed=commandline dialog
SetupIconFile=@{icon}
ArchitecturesInstallIn64BitMode=x64 ia64

[Files]
Source: "@{srcdir}\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
@{shortcuts}
Name: "{group}\Uninstall @{productname}"; Filename: "{uninstallexe}"
