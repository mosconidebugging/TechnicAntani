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

from celery import shared_task
from cachebuilder.mod_manager import *
from cachebuilder.pack_manager import *
from cachebuilder.models import Error
from api.models import *
from os import path
from cachebuilder.utils import checksum_file, build_forge, build_config, build_mod, sanitize_path, delete_built
import logging
import shutil
import pygit2
from cachebuilder.logger import DatabaseLogger
from celery import Task

class CacheBuilderTask(Task):

  def on_success(self, retval, task_id, args, kwargs):
     log = logging.getLogger("CacheBuilder")
     log.addHandler(DatabaseLogger())
     log.info("Task successfully completed")

  def on_failure(self, exc, task_id, args, kwargs, einfo):
     log = logging.getLogger("CacheBuilder")
     log.addHandler(DatabaseLogger())
     log.error(str(exc) + "\n" + einfo.traceback)

@shared_task(base=CacheBuilderTask)
def build_all_caches(user=None):
    """
    Updates all caches. Takes forever if there are many things to build
    throws FileNotFoundError if a mod we don't track is requested
    """
    log = logging.getLogger("build_all_caches")
    handle = DatabaseLogger(user)
    log.addHandler(handle)
    log.info("build_all_caches task started")

    # Read up to date data from the filesystem
    mm = ModManager(log)  # GASP!
    pm = ModpackManager(log)

    for pack in pm.list_packs():
        p = pm.get_pack(pack)
        pc = ModpackCache.objects.all().filter(slug=pack).first()

        # Create pack cache if not in the Database
        if pc is None:
            log.info("Building cache for pack %s" % pack)
            # Skip. Not a valid pack
            if p is None:
                log.error("Pack " + pack + " has errors. Fix them. Skipping.")
                continue
            pc = ModpackCache()
            pc.slug = pack
            pc.name = p.name
            pc.description = p.description
            pc.url = p.url

        log.info("Refreshing assets for pack %s." % pack)
        # Refresh md5 - just in case the images were changed
        pc.background_md5 = checksum_file(p.get_background())
        pc.logo_md5 = checksum_file(p.get_logo())
        pc.icon_md5 = checksum_file(p.get_icon())
        pc.save()

        # Copy over assets
        if not os.path.exists(os.path.join(MODBUILD_DIR, pack)):
            log.info("Asset directory does not exist")
            os.mkdir(os.path.join(MODBUILD_DIR, pack))
            os.mkdir(os.path.join(MODBUILD_DIR, pack, 'resources'))

        shutil.copy(os.path.join(MODPACKPATH, pack, 'assets', 'logo.png'), os.path.join(MODBUILD_DIR, pack,
                                                                                        'resources', 'logo_180.png'))
        shutil.copy(os.path.join(MODPACKPATH, pack, 'assets', 'icon.png'), os.path.join(MODBUILD_DIR, pack,
                                                                                        'resources', 'icon.png'))
        shutil.copy(os.path.join(MODPACKPATH, pack, 'assets', 'background.jpg'),
                    os.path.join(MODBUILD_DIR, pack, 'resources', 'background.jpg'))

        # Cycle through every version of the pack
        for packver in p.versions.keys():
            log.info("Processing version \"%s\"" % packver)
            cachedver = VersionCache.objects.all().filter(modpack=pc, version=packver).first()

            # Create cache for version if it doesn't exist - aka build it
            if cachedver is None:
                cachedver = VersionCache()
                cachedver.forgever = p.versions[packver]['forgever']
                cachedver.mcversion = p.versions[packver]['mcversion']
                cachedver.mcversion_checksum = ""  # wot
                cachedver.modpack = pc
                cachedver.version = packver
                cachedver.latest = p.latest == packver
                cachedver.recommended = p.recommended == packver
                cachedver.save()

                # Package forge as modpack.jar. We have to see what to do in the future.
                if not cachedver.forgever == "":
                    log.info("Found forge requirement: %s" % cachedver.forgever)
                    forgever = build_forge(cachedver.forgever, cachedver.mcversion, log)
                    cachedver.mods.add(forgever)

                # Package the zippone with current config in git
                confcache = build_config(pc.slug, cachedver.version,log)
                cachedver.mods.add(confcache)

            for mod in p.versions[packver]['mods'].keys():
                if mod is None:
                    log.warning("Strange. Mod is None. Skipping")
                    continue
                modcache = build_mod(mod, p.versions[packver]['mods'][mod], mm, log)
                cachedver.mods.add(modcache)
    log.removeHandler(handle)


@shared_task(base=CacheBuilderTask)
def update_modpack(repo, user):
    """
    Will update caches if new changes are pulled inn
    """
    log = logging.getLogger("update_modpack")
    log.addHandler(DatabaseLogger())
    log.info("update_modpack task started")
    repo = pygit2.Repository(path.join(MODPACKPATH, repo))
    updates = False
    for remote in repo.remotes:
        log.info("Fetching from " + remote.url)
        result = remote.fetch()
        log.info("Fetched " + str(result.received_objects) + " objects")
        if result.received_objects > 0:
            updates = True
    if not updates:
        log.warning('No updates found. Weird.')
        return False
    build_all_caches()
    return True


@shared_task(base=CacheBuilderTask)
def clone_modpack(gitrepo, targetdir):
    """
    Clones git repo in a new directory
    """
    log = logging.getLogger("clone_modpack")
    log.addHandler(DatabaseLogger())
    log.info("clone_modpack task started")
    cleandir = sanitize_path(targetdir)
    if path.isdir(path.join(MODPACKPATH, cleandir)):
        log.error('NOPE. There\'s a dir named like this.')
        return None

    pygit2.clone_repository(gitrepo, path.join(MODPACKPATH, cleandir))
    log.info("Repo created. Building")
    build_all_caches()


@shared_task(base=CacheBuilderTask)
def change_mod_repo(newrepo):
    if path.isdir(path.join(MODREPO_DIR, '.git')):
        shutil.rmtree(MODREPO_DIR)
    pygit2.clone_repository(newrepo, MODREPO_DIR)


@shared_task(base=CacheBuilderTask)
def pull_mods():
    if path.isdir(path.join(MODREPO_DIR, '.git')):
        repo = pygit2.Repository(MODREPO_DIR)
        repo.remotes[0].fetch()  # assuming first remote is best remote
        repo.checkout('refs/remotes/origin/master')


@shared_task(base=CacheBuilderTask)
def clear_caches():
    delete_built()
    clear_modpacks()
    for obj in ModCache.objects.all():
        obj.delete()
    for obj in ModInfoCache.objects.all():
        obj.delete()


@shared_task(base=CacheBuilderTask)
def clear_modpacks():
    for obj in VersionCache.objects.all():
        obj.delete()
    for obj in ModpackCache.objects.all():
        obj.delete()


@shared_task(base=CacheBuilderTask)
def clear_log():
    Error.objects.all().delete()


@shared_task(base=CacheBuilderTask)
def purge_caches():
    mp = ModpackManager()
    mp.clear_packs()
    clear_caches()
