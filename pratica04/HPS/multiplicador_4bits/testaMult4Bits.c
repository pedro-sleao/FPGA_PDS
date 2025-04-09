/*
* FUNCAO : Testa a RAM do periferico 
* PROJETO: Finite Field 256 Cosine Transforms
* DATA DE CRIACAO: 27/08/2024
*/


//Do codigo basico
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include "hwlib.h"
#include "socal.h"
#include "hps.h"
#include "alt_gpio.h"
#include "hps_0.h"

//do codigo de Breno
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <time.h> 
#include <math.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#include <unistd.h>

//Feitas por mim
#include "trataHEX.h"
#include "ram.h"
#include "peripheral.h"

#define PORT_1_MEM_BASE 0x40000
#define PORT_1_ADDR_SPAN 4
#define PORT_1_MEM_SPAN PORT_1_ADDR_SPAN*32
#define CONTROL_ADDR 0
#define NUMBERS_ADDR 1
#define RESULT_ADDR 2
#define STATUS_ADDR 3

//UDP
#define N_BUF    20

int main() 
{
	// Codigo RAM
	uint32_t i;        //para iteracoes
	uint32_t entrada;        //para iteracoes
	uint32_t mem_read;
	uint32_t mem_read_lsw;
	uint32_t mem_read_msw;
	uint32_t mem_write;
	uint16_t mem_read16;
	uint8_t  mem_read8;
	peripheral dualPortRam;

	// Codigo UDP:
	int sock, length, n, flags;
	socklen_t fromlen;
	struct sockaddr_in server;
	struct sockaddr_in from;
	char buf[N_BUF];

	sock=socket(AF_INET, SOCK_DGRAM, 0);
	if (sock < 0) printf("Opening socket");

	length = sizeof(server);
	bzero(&server,length);
	server.sin_family=AF_INET;
	server.sin_addr.s_addr=INADDR_ANY;
	server.sin_port=htons(9090);
	if (bind(sock,(struct sockaddr *)&server,length)<0) 
	    printf("binding");
	fromlen = sizeof(struct sockaddr_in);

	printf("*---------------------------------------------------------------------\n");
	printf("* FUNCTION       : TEST MULT 4 BITS\n");
	printf("* PROJECT        : TOPICOS EM COMUNICAO 02\n");
	printf("* DATE           : 2025.1 - 04/04/2025\n");
	printf("*---------------------------------------------------------------------\n");


	printf("defining the access to the memory peripherals\n");
	dualPortRam = peripheral_create(PORT_1_MEM_BASE, PORT_1_MEM_SPAN);
	//port02 = peripheral_create(PORT_2_MEM_BASE, PORT_2_MEM_SPAN);

	while(1)
	{
		printf("Aguardando pacote do PC...\n");
		bzero(buf,N_BUF);
	   	n = recvfrom(sock,buf,N_BUF,0,(struct sockaddr *)&from,&fromlen);
	   	if (n < 0) printf("recvfrom");
	   	else
	   	{   
			unsigned int A, B;
			unsigned int result;

            buf[n] = '\0';

            int k = sscanf(buf, "%d %d", &A, &B);
			printf("Reset control bit\n");
			peripheral_write32(dualPortRam, CONTROL_ADDR, 0x0);
			printf("Writing numbers...\n");
			peripheral_write32(dualPortRam, NUMBERS_ADDR, ((B & 0xF) << 4)| (A & 0xF));
			printf("Set control bit\n");
			peripheral_write32(dualPortRam, CONTROL_ADDR, 0x1);

			while(!peripheral_read32(dualPortRam,STATUS_ADDR));

			result = peripheral_read32(dualPortRam, RESULT_ADDR);

			char result_buf[sizeof(result)];
			sprintf(result_buf, "%d", result);

			printf("Reading the RAM:\n");
			for(i = 0; i < PORT_1_ADDR_SPAN; i++)
			{
				usleep(100);
				mem_read =  peripheral_read32(dualPortRam,i);
				printf("Endereco: %X, Valor: %X\n", 4*i, mem_read);
				
			}
			
			printf("Devolvendo pacote recebido:\n");
			n = sendto(sock,result_buf, strlen(result_buf)+1,0,(struct sockaddr *)&from,fromlen);
			if (n  < 0) printf("sendto");	

			printf("Enviado: '%s' (%d bytes)\n", result_buf, n);
		}
	}	
}
