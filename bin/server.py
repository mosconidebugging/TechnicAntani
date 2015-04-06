#!/usr/bin/python3

import json
from urllib.request import urlopen, urlretrieve
import sys
import shutil
import os
import zipfile

def fetch_forge(version, mcver):
    """
    Fetches forge from files.minecraftforge.org and returns the
    path it was saved into
    """
    print("Fetching forge v" + version)
    url = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/" + mcver + "-" + version + "/forge-" + mcver + "-" + version + "-universal.jar"
    (tpath, message) = urlretrieve(url)
    if message.get_content_type() != "application/java-archive":
        print("Cannot find url " + url)
        return None
    return tpath

try:
    data = urlopen(sys.argv[1]).read()
    obj = json.loads(data.decode('utf-8'))
except ValueError:
    print("Cannot GET that url, or not valid json. Error:%s" % sys.exc_info()[0])
    sys.exit(1)
except IndexError:
    print("Will download components of a modpack and unpack it.\n"
          "\tYou still have to remove clientside mods.\n"
          "Usage: server.py <SolderApiURL>/modpack/<modpackname>/<version>")
    sys.exit(2)

forgefile = fetch_forge(obj['forge'], obj['minecraft'])

if not forgefile:
    sys.exit(1)

shutil.move(forgefile, "minecraft-forge.jar")


for mod in obj['mods']:
    url = mod['url'].replace('\\\\/', '/')
    print(url, end='')
    print(" Downloading....", end='', flush=True)
    (tpath, message) = urlretrieve(url)
    if message.get_content_type() != 'application/zip':
        print("Error downloading " + url)
        os.unlink(tpath)
    print("Extracting....", end='', flush=True)
    z = zipfile.ZipFile(tpath)
    z.extractall()
    print("Done!")