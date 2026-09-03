# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Linus Jahn <lnj@kaidan.im>

import unittest

import CraftTestBase
from CraftCore import CraftCore
from Utils.StageLogger import StageLogger


class StageLoggerTest(CraftTestBase.CraftTestBase):
    def dumpLines(self, lineCount: int, lineLimit: int) -> list:
        CraftCore.settings.set("ContinuousIntegration", "OutputOnFailureLineLimit", lineLimit)
        with StageLogger("test/dump") as log:
            for i in range(lineCount):
                StageLogger.log(f"line {i}\n")
            with self.assertLogs(CraftCore.log, level="INFO") as logs:
                log.dump()
        return [record.getMessage() for record in logs.records]

    def test_dumpBelowLimit(self):
        lines = self.dumpLines(100, 1000)
        self.assertEqual(lines, [f"line {i}" for i in range(100)])

    def test_dumpTruncatesToLastLines(self):
        lines = self.dumpLines(5000, 1000)
        self.assertIn("Showing the last 1000 of 5000 lines", lines[0])
        self.assertEqual(lines[1:], [f"line {i}" for i in range(4000, 5000)])

    def test_dumpLimitCanBeDisabled(self):
        lines = self.dumpLines(2000, 0)
        self.assertEqual(lines, [f"line {i}" for i in range(2000)])


if __name__ == "__main__":
    unittest.main()
