#############################################################################
#                                                                           #
#    This program is free software: you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License as published by   #
#    the Free Software Foundation, either version 3 of the License, or      #
#    (at your option) any later version.                                    #
#                                                                           #
#    This program is distributed in the hope that it will be useful,        #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                           #
#############################################################################

from TechnicAntani.settings import MODPACKPATH
import os.path as path
from os import listdir
import json
import pygit2
import re
import sys
import logging

class Modpack:
    error = None
    log = logging.getLogger("ModPack")

    def __init__(self, name, log=None):
        self.name = name
        if log is not None:
            self.log = log
        self.log.info("Initializing ModPack \"%s\"" % name)
        mainkeys = [
            'description', 'url', 'version'
        ]


        modvers = [
            'version'
        ]
        try:
            meta = open(path.join(MODPACKPATH, name, "modpack.json"))
            self.repo = pygit2.Repository(path.join(MODPACKPATH, name))
            obj = json.load(meta)
            meta.close()
            for mkey in mainkeys:
                setattr(self, mkey, obj[mkey])
            self.versions = {}

            self.repo.checkout('refs/remotes/origin/master')  # development
            self.latest = self._read_version_only()
            self.repo.checkout('refs/remotes/origin/stable')
            self.recommended = self._read_version_only()

            tags_re = re.compile('^refs/tags/(.+)$')
            for ref in self.repo.listall_references():
                m = tags_re.match(ref)
                if m is not None:
                    self._append_version(ref)
        except IOError:
            self.log.error("Cannot read modpack.json!")
            self.error = sys.exc_info()[0]
        except KeyError:
            self.log.error("Cannot find a required key", exc_info=True)

    def _read_version_only(self):
        try:
            meta = open(path.join(MODPACKPATH, self.name, "modpack.json"))
            obj = json.load(meta)
            ver = obj["version"]
            meta.close()
            return ver
        except Exception:
            self.log.error("Cannot read version from file!", exc_info=True)
            self.error = sys.exc_info()[0]

    def _append_version(self, ref):
        try:
            self.repo.checkout(ref)
            meta = open(path.join(MODPACKPATH, self.name, "modpack.json"))
            obj = json.load(meta)
            meta.close()
            out = {}
            versionkeys = [
                'mcversion', 'forgever', 'version'
            ]
            for v in versionkeys:
                out[v] = obj[v]
            out['mods'] = {}
            for mod in obj['mods'].keys():
                out["mods"][mod] = obj["mods"][mod]
            self.versions[out['version']] = out
        except Exception:
            self.log.warning("Cannot read modpack info from ref %s. WIll skip." % ref, exc_info=True)
            self.error = sys.exc_info()[0]

    def get_background(self):
        return path.join(MODPACKPATH, self.name, "assets", "background.jpg")

    def get_logo(self):
        return path.join(MODPACKPATH, self.name, "assets", "logo.png")

    def get_icon(self):
        return path.join(MODPACKPATH, self.name, "assets", "icon.png")

    def get_versions(self):
        return self.versions.keys()

    def get_version(self, version):
        return self.versions[version]

    def get_mods(self, version):
        return self.versions[version]['mods']


class ModpackManager:
    """
    Lazy loader for modpack data
    """
    packs = {}
    log = logging.getLogger("ModpackManager")

    def __init__(self, log=None):
        """
        Initialize in a VERY lazy way
        """
        if log is not None:
            self.log = log
        for dirf in listdir(MODPACKPATH):
            if path.isdir(path.join(MODPACKPATH, dirf)):
                self.log.info("Found modpack \"%s\"" % dirf)
                self.packs[dirf] = None

    def get_pack(self, name):
        """
        Loads the Modpack data or gets it from the cache
        """
        ret = None
        if self.packs[name] is None:
            self.packs[name] = Modpack(name, self.log)
            ret = self.packs[name]
        else:
            ret = self.packs[name]
        return ret

    def list_packs(self):
        return self.packs.keys()
