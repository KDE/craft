# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>

from pathlib import Path
from tempfile import TemporaryDirectory

class Dos2UnixFile(object):
    def __init__(self, filePath : Path):
        self.filePath = filePath
        self._tmp = None
        self._unixFilePath = None


    @property
    def unixFilePath(self) -> Path:
        # TODO: find in memory solution
        if not self._unixFilePath:
            self._tmp = TemporaryDirectory()
            self._unixFilePath = Path(self._tmp.name) / self.filePath.name
            with self.filePath.open("rt", newline=None) as patch, self._unixFilePath.open("wt", newline="\n") as tmpFile:
                tmpFile.write(patch.read())
        return self._unixFilePath

    def __enter__(self) -> Path:
        return self.unixFilePath

    def __exit__(self, exc_type, exc_value, trback):
        if self._tmp:
            self._tmp.cleanup()
