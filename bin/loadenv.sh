#! /bin/bash
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

if which "pwsh" >/dev/null; then
  pwsh -C "./loadenv.ps1 && bash"
else
  echo "TODO implement loading using jq"
  exit 1
fi