#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 08:48:05 2025

@author: pedro
"""

import socket

serverAddressPort   = ("10.42.0.223", 9090) 

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

polys = ["00100200300010203303010008802222", "00000001000200030004000500060007",
         "00100020003000400050010020003222"]

for i in range(len(polys)):
    msgFromClient       = f"{polys[i]}"
    bytesToSend         = str.encode(msgFromClient)
    bufferSize          = len(bytesToSend)
    
    print("Mensagem  a ser enviada:", msgFromClient)
    
    print("Enviando a mensagem pelo socket criado")
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
    print("Esperando receber algo:")
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    
    print("Mensagem recebida:")
    msg = "Resultado {}".format(msgFromServer[0])
    print(msg)

