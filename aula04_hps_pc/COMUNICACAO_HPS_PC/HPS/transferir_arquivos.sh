#!/bin/bash
PASTA_LOCAL="./testaUDP"
IP_DESTINO="root@192.168.0.101"
PASTA_DESTINO="testaUDP"
echo "Subindo Arquivos do Projeto - $PASTA_LOCAL:"
scp $PASTA_LOCAL/* $IP_DESTINO:/home/root/$PASTA_DESTINO
echo "Subindo Bibliotecas comuns a todos os projetos:"
scp ./INC/* $IP_DESTINO:/home/root/INC


