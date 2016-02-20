from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models import ModpackCache
from api.views import get_root_for
import pygit2

@login_required
def index(request):
    context = {
        "packs": ModpackCache.objects.all(),
        "rootdir": get_root_for(request, "", ""),
        "git_ssh": not (pygit2.features & pygit2.GIT_FEATURE_SSH),
        "git_https": not (pygit2.features & pygit2.GIT_FEATURE_HTTPS)
    }
    return render(request, "dashboard/index.html", context)
