import re
from distutils.version import Version, LooseVersion, StrictVersion

import CraftDebug


class CraftVersion(Version):
    component_re = re.compile(r"(\d+ | [a-z]+ | \.| -)", re.VERBOSE)
    invalid_re = re.compile(r"^v", re.IGNORECASE)
    # we can't compare "master" with "feature1" so mark branches as larger than version
    isBranch_re = re.compile(r"^[a-z]+$", re.IGNORECASE)

    def __init__(self, version):
        Version.__init__(self, version)
        self.versionstr = version
        self.isBranch = CraftVersion.isBranch_re.match(self.versionstr)

    def __str__(self):
        return self.versionstr

    def __repr__(self):
        return "CraftVersion ('%s')" % self.versionstr

    def _cmp(self, other):
        if not isinstance(other, CraftVersion):
            raise TypeError("Can't compare CraftVersion with %s" % type(other))
        if self.isBranch or other.isBranch:
            return 0 if (self.versionstr == other.versionstr or (self.isBranch and other.isBranch)) \
                else 1 if self.isBranch and not other.isBranch else -1
        return 0 if self.version == other.version else -1 if self.version < other.version else 1

    @property
    def strictVersion(self):
        v = CraftVersion.invalid_re.sub("", self.versionstr)
        if self.isBranch or not re.match(r"^\d+.*", v):
            CraftDebug.CraftCore.log.warn(
                "Can't convert %s to StrictVersion, please use release versions for packaging" % self.versionstr,
                stack_info=True)
            return StrictVersion("0.0.0")
        loose = LooseVersion(v)
        out = []
        for entry in loose.version:
            if type(entry) is str:
                # TODO: how to convert multi char values
                val = ""
                for c in entry:
                    val += str(int(ord(c) - ord("a")))
                if len(out) > 0:
                    out[-1] += val
                else:
                    out.append(val)
            else:
                out.append(str(entry))

        vstring = ".".join(out[0: min(len(out), 3)])
        if len(out) > 3:
            vstring += "".join(out[3:])
        return StrictVersion(vstring)

    def parse(self, s):
        """
        Based on https://bitbucket.org/pypa/setuptools/src/a3d16c5f7443ec6e5e4d8d4791682b56130b41b5/pkg_resources.py?at=default

        Convert a version string to a chronologically-sortable key

         This is a rough cross between distutils' StrictVersion and LooseVersion;
         if you give it versions that would work with StrictVersion, then it behaves
         the same; otherwise it acts like a slightly-smarter LooseVersion. It is
         *possible* to create pathological version coding schemes that will fool
         this parser, but they should be very rare in practice.

         The returned value will be a tuple of strings.  Numeric portions of the
         version are padded to 8 digits so they will compare numerically, but
         without relying on how numbers compare relative to strings.  Dots are
         dropped, but dashes are retained.  Trailing zeros between alpha segments
         or dashes are suppressed, so that e.g. "2.4.0" is considered the same as
         "2.4". Alphanumeric parts are lower-cased.

         The algorithm assumes that strings like "-" and any alpha string that
         alphabetically follows "final"  represents a "patch level".  So, "2.4-1"
         is assumed to be a branch or patch of "2.4", and therefore "2.4.1" is
         considered newer than "2.4-1", which in turn is newer than "2.4".

         Strings like "a", "b", "c", "alpha", "beta", "candidate" and so on (that
         come before "final" alphabetically) are assumed to be pre-release versions,
         so that the version "2.4" is considered newer than "2.4a1".

         Finally, to handle miscellaneous cases, the strings "pre", "preview", and
         "rc" are treated as if they were "c", i.e. as though they were release
         candidates, and therefore are not as new as a version string that does not
         contain them, and "dev" is replaced with an '@' so that it sorts lower than
         than any other pre-release tag.
         """

        # remove leading characters like tag markers etc ("v5.8.0" == "5.8.0")
        s = CraftVersion.invalid_re.sub("", s)

        parts = []
        for part in self.__parse_version_parts(s.lower()):
            if part.startswith('*'):
                if part < '*final':  # remove '-' before a prerelease tag
                    while parts and parts[-1] == '*final-': parts.pop()
                # remove trailing zeros from each series of numeric parts
                while parts and parts[-1] == '00000000':
                    parts.pop()
            parts.append(part)
        self.version = tuple(parts)

    def __parse_version_parts(self, s):
        replace = {'pre': 'c', 'preview': 'c', '-': 'final-', 'rc': 'c', 'dev': '@'}.get
        for part in CraftVersion.component_re.split(s):
            part = replace(part, part)
            if not part or part == '.':
                continue
            if part[:1] in '0123456789':
                yield part.zfill(8)  # pad for numeric comparison
            else:
                yield '*' + part

        yield '*final'  # ensure that alpha/beta/candidate are before final
