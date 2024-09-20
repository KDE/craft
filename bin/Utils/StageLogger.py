# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import io
import tempfile
from typing import Optional

from CraftCore import CraftCore


class StageLogger(object):
    ActiveLogs: list["StageLogger"] = []

    def __init__(self, name: str, buffered: bool = False, outputOnFailure: bool = False):
        self.__logFile: Optional[io.TextIOBase] = None
        self._logPath = (CraftCore.standardDirs.logDir() / name).with_suffix(".log")
        self.buffered = buffered
        self.outputOnFailure = outputOnFailure
        if not self._logPath.parent.exists():
            self._logPath.parent.mkdir(parents=True)
        # delete previous log
        if self._logPath.exists():
            self._logPath.unlink()

    def __open(self, mode):
        assert not self.__logFile
        if not self.buffered:
            self.__logFile = self._logPath.open(mode, encoding="UTF-8", newline="\n")
        else:
            # write 10 mb to ram then use a file
            self.__logFile = tempfile.SpooledTemporaryFile(mode=mode, max_size=10000000, encoding="UTF-8", newline="\n")

    def write(self, s: str):
        # only create the log file if anything is written
        if not self.__logFile:
            self.__open("wt+")
        assert self.__logFile
        self.__logFile.write(s)

    def dump(self):
        if self.__logFile:
            pos = self.__logFile.tell()
            self.__logFile.seek(0)
            for line in self.__logFile.readlines():
                # linebased printing as workaround for gitlab logs dropping logs
                CraftCore.log.info(line.strip())
            assert self.__logFile.tell() == pos
            self.__logFile.seek(pos)

    def __enter__(self):
        if StageLogger.ActiveLogs:
            activeLog = StageLogger.ActiveLogs[-1]
            # TODO
            # close non active log, this allow packaging the log on Windows
            if activeLog.__logFile and not activeLog.buffered:
                activeLog.__logFile.close()
                activeLog.__logFile = None
        StageLogger.ActiveLogs.append(self)
        return self

    def __exit__(self, exc_type, exc_value, trback):
        StageLogger.ActiveLogs.remove(self)
        if self.__logFile:
            if StageLogger.ActiveLogs:
                # append to parent log
                activeLog = StageLogger.ActiveLogs[-1]
                if not activeLog.buffered:
                    activeLog.__open("at+")
                line = "*" * CraftCore.debug.lineWidth
                activeLog.write(f"\n{line}\n{self._logPath.name}\n{line}\n")
                self.__logFile.seek(0)
                while True:
                    chunk = self.__logFile.read(1024)
                    if not chunk:
                        break
                    activeLog.write(chunk)
            self.__logFile.close()

    @staticmethod
    def log(s: str):
        if StageLogger.ActiveLogs:
            StageLogger.ActiveLogs[-1].write(s)

    @staticmethod
    def logLine(s: str):
        StageLogger.log(f"{s}\n{'=' * CraftCore.debug.lineWidth}\n")

    @staticmethod
    def isOutputOnFailure():
        if StageLogger.ActiveLogs and StageLogger.ActiveLogs[-1].outputOnFailure:
            return True
        return CraftCore.settings.getboolean("ContinuousIntegration", "OutputOnFailure", False)
