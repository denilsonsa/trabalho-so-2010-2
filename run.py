#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import sys
import os.path
import subprocess

if __name__ == '__main__':

    if sys.version_info[0] != 2:
        print "AVISO! Este trabalho requer Python 2.6"
        print "AVISO! Este trabalho não funcionará no Python 3.x"
        print "Tentando rodar mesmo assim..."

    basedir = os.path.abspath(os.path.dirname(__file__))
    webserver = None
    dbserver = None

    try:
        print "Starting dbserver"
        dbserver = subprocess.Popen(
            ['java', 'br.ufrj.dcc.so.cinema.ListenerThread'],
            cwd=os.path.join(basedir, 'dbserver')
        )

        print "Starting webserver"
        webserver = subprocess.Popen(
            ['python', 'webserver.py'],
            cwd=os.path.join(basedir, 'webserver')
        )

        dbserver.wait()
        webserver.wait()
    except KeyboardInterrupt:
        pass
    finally:
        if dbserver:
            print "Terminating dbserver"
            dbserver.terminate()
        if webserver:
            print "Terminating webserver"
            webserver.terminate()
