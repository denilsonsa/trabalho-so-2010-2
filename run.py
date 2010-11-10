#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import os.path
import subprocess

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    webserver = None

    try:
        print "Starting webserver"
        webserver = subprocess.Popen(
            ['./webserver.py'],
            cwd=os.path.join(basedir, 'webserver')
        )
        webserver.wait()
    except:
    #except KeyboardInterrupt:
        if webserver:
            print "Terminating webserver"
            webserver.terminate()

