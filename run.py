#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import subprocess

if __name__ == '__main__':
    webserver = None

    try:
        print "Starting webserver"
        webserver = subprocess.Popen(['./webserver.py'], cwd='./webserver')
        webserver.wait()
    except:
    #except KeyboardInterrupt:
        if webserver:
            print "Terminating webserver"
            webserver.terminate()

