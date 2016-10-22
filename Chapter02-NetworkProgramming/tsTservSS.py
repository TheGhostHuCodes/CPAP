#!/usr/bin/env python3

from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 21567
ADDR = (HOST, PORT)


class MyRequestHandler(SRH):
    def handle(self):
        print("...connected from: ", self.client_address)
        self.wfile.write("[{}] {}".format(ctime(), self.rfile.readline()
                                          .decode('utf8')).encode('utf-8'))


tcpServ = TCP(ADDR, MyRequestHandler)
print("waiting for connection...")
tcpServ.serve_forever()
