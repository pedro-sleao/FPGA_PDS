#!/bin/bash
PASTA_LOCAL="./ntt"
IP_DESTINO="root@10.42.0.236"
PASTA_DESTINO="projeto_8ntt"
echo "Subindo Arquivos do Projeto - $PASTA_LOCAL:"
scp $PASTA_LOCAL/* $IP_DESTINO:/home/root/$PASTA_DESTINO
echo "Subindo Bibliotecas comuns a todos os projetos:"
scp ./INC/* $IP_DESTINO:/home/root/INC


