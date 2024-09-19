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
        if b is None:
            self.value = False
        elif isinstance(b, bool):
            self.value = b
        elif isinstance(b, str):
            self.value = configparser.ConfigParser.BOOLEAN_STATES.get(b.lower())
        elif isinstance(b, int):
            self.value = bool(b)
        elif isinstance(b, CraftBool):
            self.value = b.value
        else:
            raise Exception(f"Failed to cast: {type(b)} to CraftBool")

    @property
    def asOnOff(self):
        return "ON" if self.value else "OFF"

    @property
    def asYesNo(self):
        return "yes" if self.value else "no"

    @property
    def asEnableDisable(self):
        return "enable" if self.value else "disable"

    def __bool__(self) -> bool:
        return self.value

    def __eq__(self, other) -> bool:
        return self.value == other

    def __str__(self):
        return str(self.value)
