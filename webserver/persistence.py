# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

from itertools import takewhile
from base64 import b64decode, b64encode
import cPickle as pickle
import socket


PERSISTENCE_SERVER_ADDRESS = ("127.0.0.1", 1234)


class Connection(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(PERSISTENCE_SERVER_ADDRESS)
        self.read_file_like = self.sock.makefile("rb")
        self.write_file_like = self.sock.makefile("wb")

    def close(self):
        "Fecha a conexão"
        self.read_file_like.close()
        self.sock.close()

    def acquire(self):
        "Inicia uma transação, adquirindo um semáforo global."
        self.sock.sendall("ACQUIRE\n")

    def release(self):
        "Libera o semáforo previamente adquirido."
        self.sock.sendall("RELEASE\n")

    def get(self, name):
        "Retorna a string que foi salva no dbserver."
        # Esta função remove "trailing newlines" da string retornada.
        self.sock.sendall("GET {0}\n".format(name))
        return "".join(
            takewhile(
                lambda line: line.strip() != "###",
                self.read_file_like
            )
        ).rstrip("\n")

    def load(self, name):
        """Retorna o objeto salvo no dbserver (usando pickle).
        Retorna None caso a resposta seja vazia (objeto não encontrado).
        """
        s = self.get(name)
        if s:
            return pickle.loads(b64decode(s))
        else:
            return None

    def put(self, name, data):
        "Salva uma string no dbserver."
        self.sock.sendall("PUT {0}\n".format(name))
        self.sock.sendall(data)
        self.sock.sendall("\n###\n")

    def save(self, name, obj):
        "Salva um objeto no dbserver (usando pickle)."
        dump = pickle.dumps(obj)
        self.put(name, b64encode(dump))

