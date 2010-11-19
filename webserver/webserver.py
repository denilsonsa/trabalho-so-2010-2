#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import web
from models import Sessao


urls = (
    r'/', 'homepage',
    r'/sessoes', 'sessoes',
    r'/sessao/(\d+)', 'sessao',
    r'/comet', 'comet',
)
# "/static/" directory is automatically served by web.py

render = web.template.render('templates/', base='base')


class homepage:
    def GET(self):
        return render.index()
        #return u'Hello, Thomé!'


class sessoes:
    def GET(self):
        return render.listar_sessoes(sorted(Sessao(randomize=True) for i in range(10)))


class sessao:
    def GET(self, id):
        s = Sessao(randomize=True)
        return render.exibir_sessao(s)


class comet:
    def GET(self):
        # Based on:
        # http://yoan.dosimple.ch/blog/2007/11/30/
        # http://groups.google.com/group/webpy/browse_thread/thread/a12348390931b426
        # http://en.wikipedia.org/wiki/Comet_(programming)
        yield "This is a padding text...\n" * 60
        import time
        for i in range(100):
            time.sleep(1)
            yield "%d\n" % (i,)


# Debugging is automatically enabled in the built-in webserver
#web.config.debug = False

# Initializing the web.py module...
app = web.application(urls, globals())

def main():
    app.internalerror = web.debugerror
    app.run()

if __name__ == '__main__':
    main()
