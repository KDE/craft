# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>

# Executed with the python used by PipBuildSystem, prints the unsatisfied requirements as json.
# As we use --no-build-isolation and --no-deps, all requirements must be provided by craft.
#
# usage:
#   pipcheckrequirements.py build <source dir>
#   pipcheckrequirements.py build-pypi <name> <version>
#   pipcheckrequirements.py runtime <path to METADATA>

import email.parser
import importlib.metadata
import io
import json
import ssl
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

try:
    from packaging.requirements import Requirement
except ImportError:
    from pip._vendor.packaging.requirements import Requirement

if sys.version_info >= (3, 11):
    import tomllib
else:
    from pip._vendor import tomli as tomllib

try:
    import certifi
except ImportError:
    from pip._vendor import certifi

# use the same certificates as pip, the default ones of the craft python might not be usable
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

# the PEP 517 fallback for projects without a build-system table, wheel is part of setuptools nowadays
DEFAULT_BUILD_REQUIRES = ["setuptools>=40.8.0"]


def buildRequires(pyproject: str | None) -> list[str]:
    if pyproject is None:
        return DEFAULT_BUILD_REQUIRES
    return tomllib.loads(pyproject).get("build-system", {}).get("requires", DEFAULT_BUILD_REQUIRES)


def pyprojectFromSdist(data: bytes, fileName: str) -> str | None:
    # the sdist contains a single top level directory
    if fileName.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for name in archive.namelist():
                if name.count("/") == 1 and name.endswith("/pyproject.toml"):
                    return archive.read(name).decode()
    else:
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            for name in archive.getnames():
                if name.count("/") == 1 and name.endswith("/pyproject.toml"):
                    return archive.extractfile(name).read().decode()
    return None


def pyprojectFromPyPi(name: str, version: str) -> str | None:
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", context=SSL_CONTEXT) as response:
        info = json.load(response)
    sdists = [url for url in info["urls"] if url["packagetype"] == "sdist"]
    if not sdists:
        raise Exception(f"No sdist found for {name}=={version}")
    with urllib.request.urlopen(sdists[0]["url"], context=SSL_CONTEXT) as response:
        return pyprojectFromSdist(response.read(), sdists[0]["filename"])


def unsatisfied(requirements: list[str]) -> list[dict]:
    out = []
    for requirementString in requirements:
        requirement = Requirement(requirementString)
        # we don't install extras
        if requirement.marker and not requirement.marker.evaluate({"extra": ""}):
            continue
        try:
            installed = importlib.metadata.version(requirement.name)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        if installed is None or not requirement.specifier.contains(installed, prereleases=True):
            out.append({"name": requirement.name, "requirement": str(requirement), "installed": installed})
    return out


def main(args: list[str]) -> int:
    mode = args[0]
    if mode == "build":
        pyproject = Path(args[1]) / "pyproject.toml"
        requirements = buildRequires(pyproject.read_text(encoding="utf-8") if pyproject.exists() else None)
    elif mode == "build-pypi":
        requirements = buildRequires(pyprojectFromPyPi(args[1], args[2]))
    elif mode == "runtime":
        metadata = email.parser.Parser().parsestr(Path(args[1]).read_text(encoding="utf-8"), headersonly=True)
        requirements = metadata.get_all("Requires-Dist") or []
    else:
        raise Exception(f"Unknown mode {mode}")
    print(json.dumps(unsatisfied(requirements)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
