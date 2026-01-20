import os

import utils
from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.MacBasePackager import MacBasePackager
from Utils import CodeSign, CraftHash


class MacDMGPackager(MacBasePackager):
    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.dmg"
        return defines

    def createPackage(self):
        """create a package"""
        CraftCore.log.debug("packaging using the MacDMGPackager")

        defines = self.setDefaults(self.defines)
        # TODO: provide an image with dbg files
        if not self.internalCreatePackage(defines):
            return False
        appPath = self.getMacAppPath(defines)
        if not appPath:
            return False

        CraftCore.log.info(f"Packaging {appPath}")

        dmgDest = defines["setupname"]
        if os.path.exists(dmgDest):
            utils.deleteFile(dmgDest)

        dmgSettings = self.workDir() / f"{self.package.name}-dmgbuild.py"
        with dmgSettings.open("w", encoding="UTF-8") as tmp:
            tmp.write(
                f"""
# https://dmgbuild.readthedocs.io/en/latest/example.html
import os
import plistlib

application = "{appPath}"
appname = os.path.basename(application)

def icon_from_app(app_path):
    plist_path = os.path.join(app_path, "Contents", "Info.plist")
    with open(plist_path, "rb") as f:
        plist = plistlib.load(f)
    icon_name = plist["CFBundleIconFile"]
    icon_root, icon_ext = os.path.splitext(icon_name)
    if not icon_ext:
        icon_ext = ".icns"
    icon_name = icon_root + icon_ext
    return os.path.join(app_path, "Contents", "Resources", icon_name)

files = [ application ]
badge_icon = icon_from_app(application)

symlinks = {{"Applications": "/Applications"}}

icon_locations = {{appname: (140, 120), "Applications": (500, 120)}}

background = "builtin-arrow"
window_rect = ((100, 100), (640, 280))
default_view = "icon-view"

arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = "bottom"  # or 'right'
text_size = 16
icon_size = 128


format = "ULMO"
"""
            )

        if not utils.system(
            [
                "dmgbuild",
                "-s",
                dmgSettings,
                os.path.basename(dmgDest)[:-4],
                dmgDest,
            ]
        ):
            return False

        if not CodeSign.signMacPackage(dmgDest):
            return False
        CraftHash.createDigestFiles(dmgDest)

        return True
