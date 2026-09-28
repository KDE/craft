# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Linus Jahn <lnj@kaidan.im>
import contextlib
import io
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
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                log.dump()
                return [line for line in buf.getvalue().split("\n") if line]

    def test_dumpBelowLimit(self):
        # 100 lines * 9 bytes = 900 bytes. Limit 1000.
        lines = self.dumpBytes(100, 1000)
        self.assertEqual(lines, [f"line {i:03}" for i in range(100)])

    def test_dumpTruncatesToLastBytes(self):
        with self.assertLogs(CraftCore.log, level="INFO") as logs:
            outputLines = self.dumpBytes(100, 100)
            self.assertIn("Showing the last 99b of 900b", logs.records[0].getMessage())
            self.assertEqual(outputLines, [f"line {i:03}" for i in range(89, 100)])

    def test_dumpLimitCanBeDisabled(self):
        outputLines = self.dumpBytes(100, 0)
        self.assertEqual(outputLines, [f"line {i:03}" for i in range(100)])


if __name__ == "__main__":
    unittest.main()
