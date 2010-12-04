#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import random
import web

from persistence import Connection
from models import Sala, Sessao, AssentosDaSessao, Assento


urls = (
    r'/', 'homepage',

    r'/admin', 'admin',
    r'/listar_salas/?', 'listar_salas',
    r'/cadastrar_sala/?', 'cadastrar_sala',
    r'/cadastrar_sessao/?', 'cadastrar_sessao',

    r'/sessoes/?', 'listar_sessoes',
    r'/sessao/(\d+)/?', 'sessao',
    r'/comprar/(\d+)/([a-zA-Z0-9]+),([a-zA-Z0-9]+)/?', 'comprar_assento',

    r'/comet', 'comet', # this is just a small experiment
)
# "/static/" directory is automatically served by web.py

render = web.template.render('templates/', base='base')


class homepage:
    def GET(self):
        return render.index()
        #return u'Hello, Thomé!'

class admin:
    def GET(self):
        return render.admin()


class listar_salas:
    def GET(self):
        c = Connection()
        salas = c.load("salas") or []
        c.close()
        salas.sort()
        return render.listar_salas(salas)


class cadastrar_sala:
    def get_form(self):
        form = web.form.Form(  # {{{
            web.form.Textbox(
                'nome',
                web.form.notnull,
                value="Sala 1",
                description="Nome:"
            ),
            web.form.Textbox(
                'largura',
                web.form.notnull,
                web.form.regexp('^\d+$', 'Precisa ser um valor numérico'),
                value="8",
                description="Largura:"
            ),
            web.form.Textbox(
                'altura',
                web.form.notnull,
                web.form.regexp('^\d+$', 'Precisa ser um valor numérico'),
                value="8",
                description="Altura:"
            ),
            web.form.Button(
                'Cadastrar',
                type='submit'
            )
        )  # }}}
        return form()

    def GET(self):
        f = self.get_form()
        return render.cadastrar(u'Cadastrar Sala', f)

    def POST(self):
        f = self.get_form()
        if f.validates():
            s = Sala(
                nome=f["nome"].value,
                largura=int(f["largura"].value),
                altura=int(f["altura"].value)
            )

            c = Connection()
            c.acquire()

            salas = c.load("salas") or []
            if salas:
                next_id = max(x.id for x in salas)
            else:
                next_id = 1
            s.id = next_id
            salas.append(s)

            c.save("salas", salas)
            c.release()
            c.close()
            raise web.seeother('/listar_salas')
        else:
            return render.cadastrar(u'Cadastrar Sala', f)


class listar_sessoes:
    def GET(self):
        return render.listar_sessoes(sorted(Sessao(randomize=True) for i in range(10)))


class cadastrar_sessao:
    def get_form(self):
        form = web.form.Form(  # {{{
            web.form.Textbox(
                'filme',
                web.form.notnull,
                description="Filme:"
            ),
            web.form.Textbox(
                'sala',
                web.form.notnull,
                description="Sala:"
            ),
            web.form.Textbox(
                'hora',
                web.form.notnull,
                description="Hora:"
            ),
            web.form.Textarea(
                'sinopse',
                description="Sinopse:",
                rows='3'
            ),
            web.form.Button(
                'Cadastrar',
                type='submit'
            )
        )  # }}}
        return form()

    def GET(self):
        f = self.get_form()
        return render.cadastrar(u'Cadastrar Sessão', f)

    def POST(self):
        f = self.get_form()
        if f.validates():
            return "Good!"
        else:
            return render.cadastrar(u'Cadastrar Sessão', f)


class sessao:
    def GET(self, id):
        s = Sessao(randomize=True)
        s.id = id
        a = AssentosDaSessao()
        return render.exibir_sessao(s, a)


class comprar_assento:
    def GET(self, sessao_id, assento_x, assento_y):
        s = Sessao(randomize=True)
        s.id = id
        a = Assento(assento_x, assento_y)
        return render.comprar_assento(s, a, None)

    def POST(self, sessao_id, assento_x, assento_y):
        s = Sessao(randomize=True)
        s.id = id
        a = Assento(assento_x, assento_y)
        cod_compra = u"".join(str(random.randint(0,9)) for i in range(20))
        return render.comprar_assento(s, a, cod_compra)
        #raise web.seeother('/sessao/'+str(sessao_id))


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
