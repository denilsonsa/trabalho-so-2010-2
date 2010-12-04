#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import random
import re
import web
from itertools import chain

from persistence import Connection
from models import Sala, Sessao, Assento


urls = (
    r'/', 'homepage',

    r'/admin', 'admin',
    r'/listar_salas/?', 'listar_salas',
    r'/cadastrar_sala/?', 'cadastrar_sala',
    r'/cadastrar_sessao/?', 'cadastrar_sessao',
    r'/maintenance', 'maintenance',

    r'/sessoes/?', 'listar_sessoes',
    r'/sessao/(\d+)/?', 'sessao',
    r'/comprar/(\d+)/([-_a-zA-Z0-9]+)/?', 'comprar_assento',

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


class maintenance:
    get_form = web.form.Form(  # {{{
        web.form.Textbox(
            'query_get',
            web.form.notnull,
            web.form.regexp('^[a-zA-Z0-9_]+$', 'Nome inválido'),
            description="Parâmetro do GET"
        ),
        web.form.Button(
            'GET',
            type='submit'
        )
    )  # }}}

    def GET(self):
        return render.maintenance(None, self.get_form())

    def POST(self):
        input = web.input()
        if input.has_key('flush'):
            c = Connection()
            c.acquire()
            c.put("salas", "")
            c.put("sessoes", "")
            c.release()
            c.close()
            return render.maintenance(u'O banco de dados foi apagado.', self.get_form())
        elif input.has_key('init'):
            c = Connection()
            c.acquire()
            #c.put("salas", "")
            #c.put("sessoes", "")
            c.release()
            c.close()
            return render.maintenance(u'O banco de dados foi inicializado. (Mentira! Esta função ainda não foi implementada!)', self.get_form())
        elif input.has_key('query_get'):
            form = self.get_form()
            if form.validates():
                c = Connection()
                name = form['query_get'].value
                result = c.get(name)
                c.close()
                return render.maintenance(u'GET {0}\n{1}'.format(name, result), form)
            else:
                return render.maintenance(u'Nome inválido passado para a query GET.', form)


class listar_salas:
    def GET(self):
        salas = Sala.load_salas()
        salas.sort()
        return render.listar_salas(salas)


class cadastrar_sala:
    # Aviso: Não é feita checagem por nomes duplicados.
    # Aviso: Não é possível editar ou apagar salas (porque não foi
    # implementada a interface para o usuário)

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

            salas = Sala.load_salas(c)

            if salas:
                next_id = max(x.id for x in salas) + 1
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
        sessoes = Sessao.load_sessoes()
        sessoes.sort()
        return render.listar_sessoes(sessoes)


class cadastrar_sessao:
    def get_form(self, salas=None):
        if salas is None:
            salas = Sala.load_salas()
        form = web.form.Form(  # {{{
            web.form.Textbox(
                'filme',
                web.form.notnull,
                description="Filme:"
            ),
            web.form.Dropdown(
                'sala',
                [
                    (s.id, '{0} ({1}x{2})'.format(
                        s.nome, s.largura, s.altura)
                    )
                    for s in salas
                ],
                web.form.notnull,
                description="Sala:"
            ),
            web.form.Textbox(
                'hora',
                web.form.notnull,
                web.form.regexp('^\d+:\d+$', 'Hora inválida'),
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
        c = Connection()
        c.acquire()
        salas = Sala.load_salas(c)
        f = self.get_form(salas)
        if f.validates():
            s = Sessao(
                hora=f['hora'].value,
                filme=f['filme'].value,
                sinopse=f['sinopse'].value
            )

            sala_id = int(f['sala'].value)
            s.sala = filter(lambda x: x.id == sala_id, salas)[0]
            s.generate_assentos()

            sessoes = Sessao.load_sessoes(c)
            if sessoes:
                next_id = max(x.id for x in sessoes) + 1
            else:
                next_id = 1
            s.id = next_id

            sessoes.append(s)
            c.save("sessoes", sessoes)
            c.release()
            raise web.seeother('/sessoes')
        else:
            c.release()
            return render.cadastrar(u'Cadastrar Sessão', f)


class sessao:
    def GET(self, id):
        id = int(id)
        sessoes = Sessao.load_sessoes()
        filtradas = filter(lambda x: x.id == id, sessoes)
        if len(filtradas) == 0:
            raise web.seeother('/sessoes')

        return render.exibir_sessao(filtradas[0])


class comprar_assento:
    def validar_sessao_e_assento(self, sessao_id, assento_id, sessoes):
        """Verifica se a Sessão e o Assento realmente existem, e retorna
        uma tupla com (Sessao, Assento).
        
        Em caso de algum dado inválido, redireciona para a listagem de
        sessões.
        """

        sessoes_filtradas = filter(lambda x: x.id == sessao_id, sessoes)
        if len(sessoes_filtradas) == 0:
            raise web.seeother('/sessoes')

        sessao = sessoes_filtradas[0]
        assentos_filtrados = filter(
            lambda x: x.id == assento_id,
            chain(*sessao.assentos)
        )

        if len(assentos_filtrados) == 0:
            raise web.seeother('/sessoes')
        assento = assentos_filtrados[0]

        return sessao, assento

    def GET(self, sessao_id, assento_id):
        sessao_id = int(sessao_id)
        sessoes = Sessao.load_sessoes()
        sessao, assento = self.validar_sessao_e_assento(sessao_id, assento_id, sessoes)

        return render.comprar_assento(sessao, assento, None)

    def POST(self, sessao_id, assento_id):
        sessao_id = int(sessao_id)
        c = Connection()
        c.acquire()

        sessoes = Sessao.load_sessoes(c)
        try:
            sessao, assento = self.validar_sessao_e_assento(sessao_id, assento_id, sessoes)

            if assento.estado != assento.LIVRE:
                # É... Alguém já comprou este assento.
                # Paciência, e melhor sorte da próxima vez.
                return render.comprar_assento(sessao, assento, None)

            assento.estado = assento.OCUPADO
            c.save("sessoes", sessoes)
        finally:
            c.release()
            c.close()

        # Atualmente é gerado um código de compra (que é exibido como um
        # código de barras), porém esse código não fica salvo em lugar
        # nenhum.
        cod_compra = u"".join(str(random.randint(0,9)) for i in range(20))

        return render.comprar_assento(sessao, assento, cod_compra)


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
