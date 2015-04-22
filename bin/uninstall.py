#!/usr/bin/env python
# -*- coding: utf-8 -*-
# uninstalls grabber
# https://github.com/bnomis/cygwin-update
# (c) Simon Blanchard
from __future__ import print_function

import os
import os.path
import subprocess


def launchctl_unload(path):
    argv = ['launchctl', 'unload', path]
    try:
        p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print('Exception running %s: %s' % (argv, e))
    else:
        stdout, stderr = p.communicate()
        if stdout:
            print(stdout.decode().strip())
        if stderr:
            print(stderr.decode().strip())
        p.wait()


def uninstall():

    fn = 'com.yajogo.grabber.plist'
    destdir = '/Library/LaunchDaemons'
    dest = os.path.join(destdir, fn)

    launchctl_unload(dest)

    try:
        os.remove(dest)
    except Exception as e:
        print('Exception deleting %s: %s' % (dest, e))


if __name__ == '__main__':
    uninstall()

