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

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import cachebuilder.tasks as mytasks
from cachebuilder.forms import CreatePack, get_repo_name
import json
import hmac
import hashlib
from cachebuilder.models import RepoSecret, Error
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    context = {
        'menu': 'cache_cachepacks'
    }
    return render(request, "cachebuilder/index.html", context)


@login_required
def build_caches(request):
    mytasks.build_all_caches.delay()
    return redirect(index)


@login_required
def clear_caches(request):
    mytasks.clear_caches.delay()
    return redirect(index)


@login_required
def clear_modpacks(request):
    mytasks.clear_modpacks.delay()
    return redirect(index)

@login_required
def purge_caches(request):
    mytasks.purge_caches.delay()
    return redirect(index)


@login_required
def create_modpack(request):
    context = {
        'menu': 'cache_createpack'
    }
    if request.method == 'POST':
        form = CreatePack(request.POST)
        if form.is_valid():
            mytasks.clone_modpack.delay(form.cleaned_data['gitrepo'], get_repo_name(form.cleaned_data['gitrepo']))
            context['packname'] = get_repo_name(form.cleaned_data['gitrepo'])
            secret = RepoSecret()
            secret.owner = request.user
            secret.repoName = context['packname']
            secret.secret = form.cleaned_data['secret']
            secret.save()
            return render(request, "cachebuilder/creating.html", context)
    else:
        form = CreatePack()
    context['form'] = form
    return render(request, "cachebuilder/create.html", context)


@login_required
def delete_all_logs(request):
    Error.objects.all().delete()
    return redirect("LOGS")


@login_required
def display_logs(request):
    return render(request, "cachebuilder/logs.html", {
        "logs": Error.objects.all(),
        "menu" : "cache logsviewer"
    })


@csrf_exempt
def git_webhook(request):
    try:
        obj = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return HttpResponse("Git Webhook Service. Payload is not valid json.")
    signature = request.META['HTTP_X_HUB_SIGNATURE']
    if signature is None:
        return HttpResponse("Git Webhook Service. Missing X-Hub-Signature.")
    signature = signature.split("=")[1]
    repo_name = obj['repository']['name']
    try:
        secret = RepoSecret.objects.get(repoName=repo_name)
        dig = hmac.new(secret.secret.encode('utf-8'), msg=request.body, digestmod=hashlib.sha1)
        if dig.hexdigest() == signature:
            mytasks.update_modpack.delay(repo_name, secret.owner.username)
        else:
            return HttpResponse("{ error : \"Wrong key supplied\"}")
    except RepoSecret.DoesNotExist:
        return HttpResponse("{ error : \"Repo not found\"}")
    return HttpResponse("{ message : \"Update started\" }")


@csrf_exempt
def modrepo_webhook(request):
    from TechnicAntani.antanisettings import MODREPO_PASS
    signature = request.META['HTTP_X_HUB_SIGNATURE']
    signature = signature.split("=")[1]
    secret = MODREPO_PASS
    dig = hmac.new(secret.encode('utf-8'), msg=request.body, digestmod=hashlib.sha1)
    if dig.hexdigest() == signature:
        mytasks.pull_mods.delay()
    else:
        return HttpResponse("{ error : \"Wrong key supplied\"}")
    return HttpResponse("{ message : \"Update started\" }")
