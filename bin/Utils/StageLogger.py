# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import io
from pathlib import Path

from CraftCore import CraftCore


class StageLogger(object):
    ActiveLogs = []  # type: List[StageLogger]

    def __init__(self, name: str, buffered: bool = False, outputOnFailure: bool = False):
        self.__logFile = None  # type: io.TextIOBase
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
            self.__logFile = io.StringIO(newline="\n")

    def write(self, s: str):
        # only create the log file if anything is written
        if not self.__logFile:
            self.__open("wt+")
        self.__logFile.write(s)

    def dump(self):
        pos = self.__logFile.tell()
        self.__logFile.seek(0)
        for l in self.__logFile.readlines():
            # linebased printing as workaround for gitlab logs dropping logs
            CraftCore.log.info(l.strip())
        assert self.__logFile.tell() == pos
        self.__logFile.seek(pos)

    def __enter__(self):
        if StageLogger.ActiveLogs:
            activeLog = StageLogger.ActiveLogs[-1]
            if activeLog.__logFile:
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
                activeLog.__open("at+")
                line = "*" * CraftCore.debug.lineWidth
                activeLog.write(f"\n{line}\n{self._logPath.name}\n{line}\n")
                self.__logFile.seek(0)
                while True:
                    chunk = self.__logFile.read(1024)
                    if not chunk:
                        break
                    activeLog.__logFile.write(chunk)
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
