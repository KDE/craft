# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE

import io
import os
from pathlib import Path
import shutil
import sys
import tarfile

symlinks = []

tar = tarfile.open(fileobj=sys.stdin.buffer, mode="r|")

# as we are working on a stream, we can't seek, delay the resolution util the end
tar.makelink = lambda tarinfo, targetpath: symlinks.append((tarinfo.linkname, targetpath))
tar.extractall(sys.argv[1])
tar.close()



def hardlink(src : Path, dest : Path):
    if not src.exists():
        # src does not exist yet, delay
        symlinks.append((src, dest))
        return
    print(f"Resolving link: {src} {dest}")
    if src.is_dir():
        dest.mkdir()
        with os.scandir(src) as scan:
            for f in scan:
                hardlink(Path(f.path), dest / f.name)
    else:
        os.link(src, dest)

# resolve the links and use hard links
while symlinks:
    src, dest = symlinks.pop(0) 
    src = Path(src)
    dest = Path(dest)
    if not src.is_absolute():
        src = (dest.parent / src).resolve()
    try:
        hardlink(src, dest)
    except Exception as e:
        print(src, dest, file=sys.stderr)
        print(e, file=sys.stderr)
        exit(1)