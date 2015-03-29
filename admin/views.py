from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
        system("cd " + settings.MODREPO_DIR + " && " + settings.GIT_EXEC + " pull")
    else:
        system("rm -rf " + settings.MODREPO_DIR)
        system(settings.GIT_EXEC + " clone " + settings.MODREPO_REMOTE + " " + settings.MODREPO_DIR)
    return redirect(modrepo)