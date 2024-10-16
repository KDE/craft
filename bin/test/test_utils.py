import unittest

import CraftTestBase
import utils


class UtilsTest(CraftTestBase.CraftTestBase):
    def test_splitVCSUrl(self):
        result = utils.splitVCSUrl("git://servername:path.git|4.5branch|v4.5.1")
        self.assertEqual(result, ["git://servername:path.git", "4.5branch", "v4.5.1"])

        result = utils.splitVCSUrl("git://servername:path.git||v4.5.1")
        self.assertEqual(result, ["git://servername:path.git", "", "v4.5.1"])

        # simple https url
        result = utils.splitVCSUrl("https://invent.kde.org/packaging/craft-blueprints-kde")
        self.assertEqual(result, ["https://invent.kde.org/packaging/craft-blueprints-kde", "", ""])

        # same with .git suffix
        result = utils.splitVCSUrl("https://invent.kde.org/packaging/craft-blueprints-kde.git")
        self.assertEqual(result, ["https://invent.kde.org/packaging/craft-blueprints-kde.git", "", ""])

        # https url with branch
        result = utils.splitVCSUrl("https://invent.kde.org/packaging/craft-blueprints-kde|something123|")
        self.assertEqual(result, ["https://invent.kde.org/packaging/craft-blueprints-kde", "something123", ""])

        # same with .git suffix
        result = utils.splitVCSUrl("https://invent.kde.org/packaging/craft-blueprints-kde.git|something123|")
        self.assertEqual(result, ["https://invent.kde.org/packaging/craft-blueprints-kde.git", "something123", ""])

        # https url with branch containing a slash
        result = utils.splitVCSUrl("https://invent.kde.org/packaging/craft-blueprints-kde|work/something123|")
        self.assertEqual(result, ["https://invent.kde.org/packaging/craft-blueprints-kde", "work/something123", ""])

        # same with .git suffix
        result = utils.splitVCSUrl("https://invent.kde.org/packaging/craft-blueprints-kde.git|work/something123|")
        self.assertEqual(result, ["https://invent.kde.org/packaging/craft-blueprints-kde.git", "work/something123", ""])

        # simple ssh url
        result = utils.splitVCSUrl("git@invent.kde.org:sysadmin/ci-utilities.git")
        self.assertEqual(result, ["git@invent.kde.org:sysadmin/ci-utilities.git", "", ""])

        # simple ssh url with branch
        result = utils.splitVCSUrl("git@invent.kde.org:sysadmin/ci-utilities.git|something123|")
        self.assertEqual(result, ["git@invent.kde.org:sysadmin/ci-utilities.git", "something123", ""])

        # simple ssh url with branch containing a slash
        result = utils.splitVCSUrl("git@invent.kde.org:sysadmin/ci-utilities.git|work/something123|")
        self.assertEqual(result, ["git@invent.kde.org:sysadmin/ci-utilities.git", "work/something123", ""])


if __name__ == "__main__":
    unittest.main()
