# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

from itertools import takewhile
import socket


PERSISTENCE_SERVER_ADDRESS = ("127.0.0.1", 1234)


class Connection(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(PERSISTENCE_SERVER_ADDRESS)
        self.file_like = self.sock.makefile("rb")

    def acquire(self):
        "Inicia uma transação, adquirindo um semáforo global."
        self.sock.sendall("ACQUIRE\n")

    def release(self):
        "Libera o semáforo previamente adquirido."
        self.sock.sendall("RELEASE\n")

    def get(self, name):
        # XXX: Esta função remove "trailing newlines" da string retornada.
        self.sock.sendall("GET {0}\n".format(name))
        return "".join(
            takewhile(
                lambda line: line.strip() != "###",
                self.file_like
            )
        ).rstrip("\n")

    def put(self, name, data):
        self.sock.sendall("PUT {0}\n".format(name))
        self.sock.sendall(data)
        self.sock.sendall("\n###\n")

    def close(self):
        self.file_like.close()
        self.sock.close()
