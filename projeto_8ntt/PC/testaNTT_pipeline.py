#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 10:12:42 2025

@author: pedro
"""

import socket

serverAddressPort   = ("10.42.0.21", 9090) 

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

polys = ["00100200300010203303010008802222",
        "00000001000200030004000500060007",
        "00100020003000400050010020003222",
        "00010002000300040005000600070008",
        "00110012001300140015001600170018",
        "00210022002300240025002600270028",
        "00310032003300340035003600370038",
        "00410042004300440045004600470048"]

bufferSize = len(polys)
msgFromClient = f"{bufferSize}"
bytesToSend = str.encode(msgFromClient)

print("Mensagem  a ser enviada:", msgFromClient)
print("Enviando o numero de entradas pelo socket criado")
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

print("Esperando confirmação:")
msgFromServer = UDPClientSocket.recvfrom(1)
print("Ok")

for i in range(len(polys)):
    msgFromClient       = f"{polys[i]}"
    bytesToSend         = str.encode(msgFromClient)
    bufferSize          = len(bytesToSend)
    
    print("Mensagem  a ser enviada:", msgFromClient)
    
    print("Enviando a mensagem pelo socket criado")
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
    print("Esperando confirmacao")
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

print("Entradas enviadas")

print("Esperando os resultados")
resultado = []
for i in range(len(polys)):
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    
    decodedMsg = msgFromServer[0].decode().strip("\x00")
    resultadoStrList = map(''.join, zip(*[iter(decodedMsg)]*4))
    
    resultado.append([int(i) for i in resultadoStrList])
    
print(resultado)
    
