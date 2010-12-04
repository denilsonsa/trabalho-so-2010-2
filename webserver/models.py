# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import random
import string

from persistence import Connection


class Sala(object):
    def __init__(self, id=None, nome=None, largura=None, altura=None):
        self.id = id
        self.nome = nome
        self.largura = largura
        self.altura = altura

    def __repr__(self):
        return 'Sala({0})'.format(', '.join(
            repr(getattr(self, x)) for x in
            ('id', 'nome', 'largura', 'altura',)
        ))

    def __cmp__(self, other):
        for attr in ('nome', 'id',):
            c = cmp(getattr(self, attr), getattr(other, attr))
            if c:
                return c
        return 0

    @staticmethod
    def load_salas(connection=None):
        "Retorna uma lista de objetos Sala(), carregada a partir do dbserver."
        if connection is None:
            c = Connection()
        else:
            c = connection

        salas = c.load("salas") or []

        if connection is None:
            c.close()

        return salas


class Sessao(object):
    def __init__(self, id=None, hora=None, sala=None, filme=None, sinopse=None):
        self.id = id
        self.hora = hora
        self.sala = sala
        self.filme = filme
        self.sinopse = sinopse
        self.assentos = [[]]

    def generate_assentos(self):
        self.assentos = [
            [
                Assento(
                    id="{0}-{1}".format(string.uppercase[i], j+1),
                    x=j,
                    y=i
                )
                for j in range(self.sala.largura)
            ]
            for i in range(self.sala.altura)
        ]

    def get_assentos_count(self):
        """Retorna uma tupla com a quantidade de assentos (livres, total)"""
        total1 = sum( len(l) for l in self.assentos )
        total2 = self.sala.altura * self.sala.largura
        assert total1 == total2

        livres = sum(
            len([a for a in l if a.estado == a.LIVRE])
            for l in self.assentos
        )

        return livres, total1

    def get_assentos_count_string(self):
        """Retorna 'livres/total', como string"""
        return '{0}/{1}'.format(*self.get_assentos_count())

    def __repr__(self):
        return 'Sessao({0})'.format(', '.join(
            repr(getattr(self, x)) for x in
            ('id', 'hora', 'sala', 'filme',)
        ))

    def __cmp__(self, other):
        for attr in ('hora', 'sala', 'filme', 'id',):
            c = cmp(getattr(self, attr), getattr(other, attr))
            if c:
                return c
        return 0

    @staticmethod
    def load_sessoes(connection=None):
        "Retorna uma lista de objetos Sessao(), carregada a partir do dbserver."
        if connection is None:
            c = Connection()
        else:
            c = connection

        sessoes = c.load("sessoes") or []

        if connection is None:
            c.close()

        return sessoes


class Assento(object):
    LIVRE = 0
    OCUPADO = 1

    def __init__(self, id=None, x=None, y=None, estado=None):
        if estado is None:
            estado = Assento.LIVRE

        self.id = id
        self.x = x
        self.y = y
        self.estado = estado

    def __repr__(self):
        return 'Assento({0})'.format(', '.join(
            repr(getattr(self, x)) for x in
            ('id', 'x', 'y', 'estado',)
        ))

    def __cmp__(self, other):
        for attr in ('id', 'y', 'x',):
            c = cmp(getattr(self, attr), getattr(other, attr))
            if c:
                return c
        return 0
