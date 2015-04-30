# TechnicAntani 2
[![Build Status](https://travis-ci.org/admiral0/TechnicAntani.svg?branch=master)](https://travis-ci.org/admiral0/TechnicAntani)
[![Project Stats](https://www.openhub.net/p/TechnicAntani/widgets/project_thin_badge.gif)](https://www.openhub.net/p/TechnicAntani)

## WARNING: This is an alpha version.

This is a rewrite of TechnicSolder in python-django 1.7+. It has a couple of requirements:
 * python >= 3.3
 * python-pip for python3
 * python-virtualenv for python3
 * git
 *
 * I recommend running this on Linux or OSX. Though I've coded careful enough to possibly have it running on windows
 I cannot assure it runs 100% smooth there. So you're on your own. Ah, I also happen to drop in /dev/null issues with
 windows OS unless it's a pull request.  

## Why
Because I want to bring modpack development and server management to a whole new level.

## Current Features
 * Mod repo management. The mod repo is the mod collection available to modpacks. Can be a dumb folder to sync with
  rsync, dropbox, syncthing, whatever or a git repo (not recommended)
 * Modpack management. All modpacks are got repos. Every tag on git is a version. Version on master branch is the latest
 available, stable branch is the recommended one.
 * Github hook support. You can work on your modpack without going to the web interface once. Git magic!

## Planned features (in order of priority)
 * Skeleton server pack generation
 * modpack helper scripts/gui
