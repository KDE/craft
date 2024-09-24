# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Hannah von Reth <vonreth@kde.org>
import configparser


class CraftBool(object):
    """
    Wrapper for bool
    Provides properties for integration with buildsystem flags
    """

    def __init__(self, b: bool):
        super().__init__()
        self.value = bool(b)

    @staticmethod
    def fromSetting(s: str) -> "CraftBool":
        return CraftBool(configparser.ConfigParser.BOOLEAN_STATES.get(s.lower()))

    @property
    def asOnOff(self):
        return "ON" if self.value else "OFF"

    @property
    def asYesNo(self):
        return "yes" if self.value else "no"

    @property
    def asEnableDisable(self):
        return "enable" if self.value else "disable"

    @property
    def inverted(self) -> "CraftBool":
        return CraftBool(not self)

    def __bool__(self) -> bool:
        return self.value

    def __eq__(self, other) -> bool:
        return self.value == other

    def __or__(self, other) -> "CraftBool":
        return CraftBool(self.value or other)

    def __and__(self, other) -> "CraftBool":
        return CraftBool(self.value and other)

    def __str__(self):
        return str(self.value)
