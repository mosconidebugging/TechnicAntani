from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cachebuilder.pack_manager import ModpackManager
from api.models import ModpackCache
from api.views import get_root_for

@login_required
def index(request):
    pm = ModpackManager()
    context = {
        "packs": ModpackCache.objects.all(),
        "rootdir": get_root_for(request, "", "")
    }
    return render(request, "dashboard/index.html", context)
