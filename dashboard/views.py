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
        "git_ssh": pygit2.features < 4,
        "git_https": pygit2.features < 2
    }
    return render(request, "dashboard/index.html", context)
