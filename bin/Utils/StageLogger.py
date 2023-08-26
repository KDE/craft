# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import io
from pathlib import Path

from CraftCore import CraftCore


class StageLogger(object):
    ActiveLogs = []  # type: List[StageLogger]

    def __init__(self, name: str):
        self.__logFile = None  # type: io.TextIOBase
        self._logPath = (CraftCore.standardDirs.craftRoot() / "logs" / name).with_suffix(".log")
        if not self._logPath.parent.exists():
            self._logPath.parent.mkdir(parents=True)

    def write(self, s: str):
        # only create the log file if anything is written
        if not self.__logFile:
            self.__logFile = self._logPath.open("wt", encoding="UTF-8")
        self.__logFile.write(s)

    def dump(self):
        self.__logFile.flush()
        with self._logPath.open("rt", encoding="UTF-8", newline="\n") as read:
            CraftCore.log.info(read.read())

    def __enter__(self):
        StageLogger.ActiveLogs.append(self)
        return self

    def __exit__(self, exc_type, exc_value, trback):
        StageLogger.ActiveLogs.remove(self)
        if self.__logFile:
            self.__logFile.close()

    @staticmethod
    def log(s: str):
        for l in StageLogger.ActiveLogs:
            l.write(s)

    @staticmethod
    def logLine(s: str):
        StageLogger.log(f"{s}\n{'=' * CraftCore.debug.lineWidth}\n")

    @staticmethod
    def dumpCurrentLog():
        StageLogger.ActiveLogs[-1].dump()
