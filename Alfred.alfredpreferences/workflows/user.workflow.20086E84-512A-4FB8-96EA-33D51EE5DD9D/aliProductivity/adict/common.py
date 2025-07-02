#!/usr/bin/python2.7
#-*- coding: UTF-8 -*-
#######################################################################
import os, sys, inspect


def script_abspath(frame=inspect.currentframe()):
    p = os.path.split(inspect.getfile( frame ))[0]
    absdir = os.path.realpath(os.path.abspath(p))
    return absdir


def script_abspath_parent(frame=inspect.currentframe()):
    return os.path.dirname(script_abspath(frame))


def include_dir(subdir=None, frame=inspect.currentframe()):
    # NOTES:
    # DO NOT USE __file__ !!!
    # dir = os.path.dirname(os.path.abspath(__file__))
    # __file__ fails if script is called in different ways on Windows
    # __file__ fails if someone does os.chdir() before
    # sys.argv[0] also fails because it doesn't not always contains
    #   the path
    #
    # realpath() will make your script run, even if you symlink it
    p = os.path.split(inspect.getfile( frame ))[0]
    incdir = os.path.realpath(os.path.abspath(p))
    if incdir not in sys.path:
        sys.path.insert(0, incdir)
    if subdir:
        # use this if you want to include modules from a subfolder
        incdir = os.path.realpath(os.path.abspath(os.path.join(p, subdir)))
        if incdir not in sys.path:
            sys.path.insert(0, incdir)

def dependency(absdir):
    pkgini = os.path.join(absdir, "dependency")

    if not os.path.exists(pkgini):
        return
    if os.path.isdir(pkgini):
        include_dir(pkgini)

###########################################################
# include dir and parent dirs
absdir = script_abspath()
fatherDir = absdir
while os.path.isdir(absdir):
    dependency(absdir)
    pkgini = os.path.join(absdir, "__init__.py")
    if not os.path.exists(pkgini):
        break
    if os.path.isdir(pkgini):
        break
    include_dir(absdir)
    fatherDir = absdir
    absdir = os.path.dirname(absdir)

