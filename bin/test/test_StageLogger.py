# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Linus Jahn <lnj@kaidan.im>

import unittest

import CraftTestBase
from CraftCore import CraftCore
from Utils.StageLogger import StageLogger


class StageLoggerTest(CraftTestBase.CraftTestBase):
    def dumpBytes(self, lineCount: int, byteLimit: int) -> list:
        CraftCore.settings.set("ContinuousIntegration", "OutputOnFailureLimit", byteLimit)
        with StageLogger("test/dump") as log:
            for i in range(lineCount):
                StageLogger.log(f"line {i:03}\n")
            with self.assertLogs(CraftCore.log, level="INFO") as logs:
                log.dump()
        return [record.getMessage() for record in logs.records]

    def test_dumpBelowLimit(self):
        # 100 lines * 9 bytes = 900 bytes. Limit 1000.
        lines = self.dumpBytes(100, 1000)
        self.assertEqual(lines, [f"line {i:03}" for i in range(100)])

    def test_dumpTruncatesToLastBytes(self):
        lines = self.dumpBytes(100, 100)
        self.assertIn("Showing the last 99b of 900b", lines[0])
        outputLines = [line for line in lines[1:] if line]
        self.assertEqual(outputLines, [f"line {i:03}" for i in range(89, 100)])

    def test_dumpLimitCanBeDisabled(self):
        lines = self.dumpBytes(100, 0)
        self.assertEqual(lines, [f"line {i:03}" for i in range(100)])


if __name__ == "__main__":
    unittest.main()
