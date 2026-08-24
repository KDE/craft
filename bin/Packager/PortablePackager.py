#
# copyright (c) 2011 Hannah von Reth <vonreth@kde.org>
#
import textwrap
from pathlib import Path

from CraftBase import InitGuard
from CraftCore import CraftCore

from .CollectionPackagerBase import CollectionPackagerBase
from .MacBasePackager import MacBasePackager
from .SevenZipPackager import SevenZipPackager

# on mac os we use MacBasePackager otherwise CollectionPackagerBase
_packagerBase = MacBasePackager if CraftCore.compiler.isMacOS else CollectionPackagerBase


class PortablePackager(_packagerBase, SevenZipPackager):  # type: ignore[valid-type]
    """Packager for portal 7zip archives"""

    LocalSignSh = textwrap.dedent(
        """\
        #!/bin/sh
        codesign -s - -f --deep --preserve-metadata=identifier,entitlements '{setupname}'
        """
    )

    @InitGuard.init_once
    def __init__(self, **kwargs):
        SevenZipPackager.__init__(self, **kwargs)
        _packagerBase.__init__(self, **kwargs)

    @property
    def archiveExtension(self):
        extension = "." + CraftCore.settings.get("Packager", "7ZipArchiveType", "7z")
        if extension == ".7z" and not CraftCore.compiler.isWindows:
            # .tar.xz is better supported on macos
            extension = ".tar.xz"
        return extension

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}{self.archiveExtension}"
        # TODO: we use the parent dir of foo.app, as we want the foo.app to be the root of the archive
        # however the parent dir might contain more than just foo.app
        defines["srcdir"] = self.archiveDir() if CraftCore.compiler.isWindows else self.getMacAppPath(defines).parent
        return defines

    def createPortablePackage(self, defines) -> bool:
        """create portable 7z package with digest files located in the manifest subdir"""
        if not CraftCore.settings.getboolean("CodeSigning", "Enabled", False) and CraftCore.compiler.isMacOS:
            localSign = Path(defines["srcdir"]) / "localSign.sh"
            with localSign.open("wt") as f:
                f.write(PortablePackager.LocalSignSh.format(setupname=self.getMacAppPath(defines).name))
            localSign.chmod(0o755)
        return self._createArchive(Path(defines["setupname"]).name, defines["srcdir"], self.packageDestinationDir())

    def createPackage(self):
        """create a package"""

        defines = self.setDefaults(self.defines)
        if not self.internalCreatePackage(defines):
            return False

        return self.createPortablePackage(defines)
