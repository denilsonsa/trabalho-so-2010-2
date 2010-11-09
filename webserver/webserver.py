#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import web

import random


urls = (
    '/', 'homepage',
    '/sessoes', 'sessoes'
)
# "/static/" directory is automatically served by web.py

render = web.template.render('templates/', base='base')


class homepage:
    def GET(self):
        return render.index()
        #return u'Hello, Thomé!'


class Sessao(object):
    def __init__(self, hora=None, sala=None, lugares_total=None, lugares_livres=None, filme=None, randomize=False):
        self.hora = hora
        self.sala = sala
        self.lugares_total = lugares_total
        self.lugares_livres = lugares_livres
        self.filme = filme

        if randomize:
            self.randomize()

    def randomize(self):
        self.hora = '%02d:%02d' % (random.randint(12, 23), random.randint(0, 59))
        self.sala = random.randint(1, 6)
        self.lugares_total = 60
        self.lugares_livres = random.randint(0, self.lugares_total)
        self.filme = u'A volta dos que não foram II'

    def __repr__(self):
        return 'Sessao({0})'.format(', '.join(
            repr(getattr(self, x)) for x in 
            ('hora', 'sala', 'lugares_total', 'lugares_livres', 'filme', )
        ))

    def __cmp__(self, other):
        for attr in ('hora', 'sala', 'filme', 'lugares_total', 'lugares_livres', ):
            c = cmp(getattr(self, attr), getattr(other, attr))
            if c:
                return c
        return 0


class sessoes:
    def GET(self):
        return render.listar_sessoes(sorted(Sessao(randomize=True) for i in range(10)))



# Debugging is automatically enabled in the built-in webserver
#web.config.debug = False

# Initializing the web.py module...
app = web.application(urls, globals())

def main():
    app.internalerror = web.debugerror
    app.run()

if __name__ == '__main__':
    main()
