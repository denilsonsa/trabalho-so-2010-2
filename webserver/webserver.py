#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import web
from models import Sessao


urls = (
    r'/', 'homepage',
    r'/sessoes', 'sessoes',
    r'/sessao/(\d+)', 'sessao',
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


# Debugging is automatically enabled in the built-in webserver
#web.config.debug = False

# Initializing the web.py module...
app = web.application(urls, globals())

def main():
    app.internalerror = web.debugerror
    app.run()

if __name__ == '__main__':
    main()
