#!/bin/bash
PASTA_LOCAL="./multiplicador_4bits"
IP_DESTINO="root@10.42.0.191"
PASTA_DESTINO="multiplicador_4bits"
echo "Subindo Arquivos do Projeto:"
scp $PASTA_LOCAL/* $IP_DESTINO:/home/root/tc2_fpga_pds/$PASTA_DESTINO


