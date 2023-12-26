# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import json
import os

if __name__ == "__main__":
    print(json.dumps(dict(os.environ)))
