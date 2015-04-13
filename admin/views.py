from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pygit2
import shutil

# Create your views here.
import TechnicAntani.antanisettings as settings
from os import system, path


@login_required
def modrepo(request):
    context = {
        "git_remote": settings.MODREPO_REMOTE,
        "git_secret": settings.MODREPO_PASS
    }
    return render(request, "admin/mods.html", context)


@login_required
def initialize(request):
    if path.exists(settings.MODREPO_DIR) and path.exists(path.join(settings.MODREPO_DIR, ".git")):
        repo = pygit2.Repository(settings.MODREPO_DIR)
        for remote in repo.remotes:
            if remote.name == 'origin':
                result = remote.fetch()
    else:
        shutil.rmtree(settings.MODREPO_DIR)
        pygit2.clone_repository(settings.MODREPO_REMOTE, settings.MODREPO_DIR)
    return redirect(modrepo)
