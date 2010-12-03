# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import random


class Sessao(object):
    def __init__(self, id=None, hora=None, sala=None, lugares_total=None, lugares_livres=None, filme=None, randomize=False):
        self.id = id
        self.hora = hora
        self.sala = sala
        self.lugares_total = lugares_total
        self.lugares_livres = lugares_livres
        self.filme = filme

        if randomize:
            self.randomize()

    def randomize(self):
        self.id = random.randint(1, 999999)
        self.hora = '%02d:%02d' % (random.randint(12, 23), random.randint(0, 59))
        self.sala = random.randint(1, 6)
        self.lugares_total = 60
        self.lugares_livres = random.randint(0, self.lugares_total)
        self.filme = u'A volta dos que não foram II'

    def __repr__(self):
        return 'Sessao({0})'.format(', '.join(
            repr(getattr(self, x)) for x in
            ('id', 'hora', 'sala', 'lugares_total', 'lugares_livres', 'filme', )
        ))

    def __cmp__(self, other):
        for attr in ('hora', 'sala', 'filme', 'lugares_total', 'lugares_livres', ):
            c = cmp(getattr(self, attr), getattr(other, attr))
            if c:
                return c
        return 0


class AssentosDaSessao(object):
    def __init__(self, linhas=8, colunas=8):
        self.linhas = linhas
        self.colunas = colunas
        #self.assentos = [[]]

        self.generate_assentos()

    def generate_assentos(self):
        self.assentos = [
            [Assento(j,i) for j in range(self.colunas) ]
            for i in range(self.linhas)
        ]

class Assento(object):
    LIVRE = 0
    OCUPADO = 1

    def __init__(self, x, y, estado=None):
        if estado is None:
            estado = Assento.LIVRE

        self.x = x
        self.y = y
        self.estado = estado

    def __repr__(self):
        return 'Assento({0})'.format(self.estado)
