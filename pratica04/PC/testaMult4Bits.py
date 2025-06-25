#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 11:06:17 2025

@author: pedro
"""

import socket

serverAddressPort   = ("10.42.0.162", 9090) 

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

resultado = []
for a in range(16):
    for b in range(16):
        y = a*b
        msgFromClient       = f"{a} {b}"
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
        
        resultado.append(y == int(msgFromServer[0].decode().strip("\x00")))
