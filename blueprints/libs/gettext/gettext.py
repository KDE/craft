# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # On Android we use libintl-lite instead
        # (however gettext added Adnroid support recently so maybe we should look into switching to it?)
        self.parent.package.categoryInfo.platforms |= CraftCore.compiler.Platforms.Native

    def setTargets(self):
        for ver in ["0.21", "0.22.3"]:
            self.targets[ver] = f"https://ftp.gnu.org/pub/gnu/gettext/gettext-{ver}.tar.gz"
            self.targetInstSrc[ver] = "gettext-%s" % ver
        self.targetDigests["0.21"] = (["c77d0da3102aec9c07f43671e60611ebff89a996ef159497ce8e59d075786b12"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.22.3"] = (["839a260b2314ba66274dae7d245ec19fce190a3aa67869bf31354cb558df42c7"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.21"] = [
            ("gettext-0.21-add-missing-ruby.diff", 1),
            (
                "d1836dbbd6a90b4c0ab79bc5292c023f08b49511.patch",
                1,
            ),  # https://git.savannah.gnu.org/gitweb/?p=gettext.git;a=commitdiff;h=d1836dbbd6a90b4c0ab79bc5292c023f08b49511
        ]

        if CraftCore.compiler.compiler.isMinGW:
            self.patchToApply["0.21"] += [
                ("0011-fix-interference-between-libintl-boost-header-files.patch", 1)
            ]  # https://github.com/msys2/MINGW-packages/blob/master/mingw-w64-gettext/0011-fix-interference-between-libintl-boost-header-files.patch
            self.patchLevel["0.21"] = 2

        self.patchToApply["0.22.3"] = [
            # https://github.com/msys2/MINGW-packages/blob/24837a628f692a9133705ec36590d71630f89876/mingw-w64-gettext/0021-replace-fsync.patch
            ("0021-replace-fsync.patch", 1),
            # https://raw.githubusercontent.com/vslavik/gettext-tools-windows/master/patches/gettext-0.22-0001-build-failure-on-mingw-close-module.patch
            ("gettext-0.22-0001-build-failure-on-mingw-close-module.patch", 1),
            # define unsetenv for msvc
            ("gettext-0.22.3-20231028.diff", 1),
        ]

        if CraftCore.compiler.compiler.isMSVC:
            # with msvc we need to link libxml2 not xml2
            self.patchToApply["0.22.3"] += [("msvc-fix-libxml2.diff", 1)]

        # the following patch is required to build on msvc but breaks mingw with:
        """
        make[5]: Entering directory '/d/CraftMingw/build/libs/gettext/work/build/gettext-tools/src'
        gcc -DLOCALEDIR=\"/d/CraftMingw/bin/data/locale\" -DBISON_LOCALEDIR=\"/usr/share/locale\" -DLOCALE_ALIAS_PATH=\"/d/CraftMingw/bin/data/locale\" -DUSEJAVA=0 -DGETTEXTJAR=\"/d/CraftMingw/bin/data/gettext/gettext.jar\" -DLIBDIR=\"/d/CraftMingw/lib\" -DGETTEXTDATADIR=\"/d/CraftMingw/bin/data/gettext\" -DPROJECTSDIR=\"/d/CraftMingw/bin/data/gettext/projects\" -DEXEEXT=\".exe\" -DHAVE_CONFIG_H -I. -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools/src -I..  -I. -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools/src -I.. -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools/libgrep -I../gnulib-lib -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools/gnulib-lib -I../../gettext-runtime/intl -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools/../gettext-runtime/intl -I../libgettextpo -I/d/_/5f852aa6/gettext-0.22.3/gettext-tools/libgettextpo -DINSTALLDIR=\"/d/CraftMingw/bin\"   -fdiagnostics-color=always -I/d/CraftMingw/include  -O2 -g -DNDEBUG  -c -o msgcmp-msgcmp.o `test -f 'msgcmp.c' || echo '/d/_/5f852aa6/gettext-0.22.3/gettext-tools/src/'`msgcmp.c
        In file included from D:/_/5f852aa6/gettext-0.22.3/gettext-tools/src/msgcmp.c:32:
        ../gnulib-lib/error.h:409:6: error: expected ')' before '?' token
          409 |      ? __gl_error_call1 (function, status, __VA_ARGS__)         \
              |      ^
        ../libgettextpo/error.h:480:7: note: in expansion of macro '__gl_error_call'
          480 |       __gl_error_call (error, status, __VA_ARGS__)
              |       ^~~~~~~~~~~~~~~
        ../gnulib-lib/stdio.h:349:24: note: in expansion of macro 'error'
          349 |   _GL_EXTERN_C rettype func parameters_and_attributes
              |                        ^~~~
        ../gnulib-lib/error.h:409:6: error: expected ')' before '?' token
          409 |      ? __gl_error_call1 (function, status, __VA_ARGS__)         \
              |      ^
        ../libgettextpo/error.h:540:7: note: in expansion of macro '__gl_error_call'
          540 |       __gl_error_call (error_at_line, status, __VA_ARGS__)
              |       ^~~~~~~~~~~~~~~
        ../gnulib-lib/stdio.h:349:24: note: in expansion of macro 'error_at_line'
          349 |   _GL_EXTERN_C rettype func parameters_and_attributes
        """
        if not CraftCore.compiler.compiler.isMinGW:
            # https://src.fedoraproject.org/rpms/gettext/blob/6a2dc0e302225010471d92fc1abd9938b256855a/f/gettext-0.22-disable-libtextstyle.patch
            #
            # * Fri Apr 30 2021 Sundeep Anand <suanand@redhat.com> - 0.21-5
            # - Add gettext-0.21-disable-libtextstyle.patch
            #   Do not build libtextstyle, as it depends on libcroco
            #   which is now unmaintained and has known security bugs.
            #   Obsolete libtextstyle and libtextstyle-devel packages.
            self.patchToApply["0.22.3"] += [("gettext-0.22-disable-libtextstyle.patch", 1)]
        self.patchLevel["0.22.3"] = 3

        self.description = "GNU internationalization (i18n)"
        self.defaultTarget = "0.22.3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libunistring"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        # we call it specially in configure
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += [
            "--disable-java",
            "--disable-native-java",
            "--enable-nls",
            "--enable-c++",
            "--with-included-gettext",
            "--with-included-glib",
            "--with-included-regex",
            "--with-gettext-tools",
            "--enable-relocatable",
            # preven use of buildin libxml2
            "gl_cv_libxml_force_included=no",
            "gl_cv_libxml_use_included=no",
        ]

        if CraftCore.compiler.compiler.isMSVC:
            # workaround for "'C:C:/CraftRoot/msys/CraftRoot/build/_/527d4567/gettext-0.21/gettext-runtime/libasprintf/autosprintf.cc'"
            self.subinfo.options.useShadowBuild = False
            # self.subinfo.options.configure.autoreconf = False
            # https://github.com/microsoft/vcpkg/blob/c6a4ed75f03a7485cf6fc91794809cd73f8f5aeb/ports/gettext/portfile.cmake#L49
            self.subinfo.options.configure.args += [
                "ac_cv_func_wcslen=yes",
                "ac_cv_func_memmove=yes"
                # The following are required for a full gettext built (libintl and tools).
                "gl_cv_func_printf_directive_n=no",  # segfaults otherwise with popup window
                "ac_cv_func_memset=yes",  # not detected in release builds
                "ac_cv_header_pthread_h=no",
                "ac_cv_header_dirent_h=no",
                "ac_cv_header_getopt_h=no",
            ]

    def configure(self):
        if not (
            self.shell.execute(self.sourceDir(), "libtoolize", ["--automake", "--copy", "--force"])
            and self.shell.execute(self.sourceDir(), f"{self.shell.toNativePath(self.sourceDir())}/autogen.sh", ["--skip-gnulib"])
        ):
            return False
        return super().configure()

    def postInstall(self):
        return self.patchInstallPrefix(
            [
                self.installDir() / "bin/autopoint",
                self.installDir() / "bin/gettextize",
                self.installDir() / "lib/gettext/user-email",
            ],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
