/*
* FUNCAO : Testar Comunicacao UDP
* PROJETO: TOPICOS EM COMUNICAO 02
* DATA DE CRIACAO: 25/06/2025
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
#include "trataHEX.h"
#include "utils.h"

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

//Codigo da RAM
#include "trataHEX.h"
#include "ram.h"
#include "peripheral.h"

//Codigo da ntt
#include "ntt.h"

#include <unistd.h>

//RAM
#define PORT_1_MEM_BASE 0x40400
#define PORT_1_ADDR_SPAN 18
#define PORT_1_MEM_SPAN PORT_1_ADDR_SPAN*16
#define CONTROL_ADDR 0
#define NUMBERS_ADDR_BASE 1
#define RESULT_ADDR_BASE 9
#define STAGE1_STATUS_ADDR 17
#define STAGE2_STATUS_ADDR 18
//UDP
#define N_BUF    32

int main() 
{	
	//Codigo RAM:
	uint32_t i;        //para iteracoes
	uint32_t entrada;        //para iteracoes
	uint32_t mem_read;
	uint32_t mem_read_lsw;
	uint32_t mem_read_msw;
	uint32_t mem_write;
	uint16_t mem_read16;
	uint8_t  mem_read8;
	peripheral dualPortRam;

	//Codigo UDP:
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
	//

	printf("*---------------------------------------------------------------------\n");
	printf("* FUNCTION       : UDP COMMUNICATION TEST\n");
	printf("* PROJECT        : TOPICOS EM COMUNICAO 02\n");
	printf("* DATE           : 2025.1 - 25/06/2025\n");
	printf("*---------------------------------------------------------------------\n");

	printf("defining the access to the memory peripherals\n");
	dualPortRam = peripheral_create(PORT_1_MEM_BASE, PORT_1_MEM_SPAN);

    printf("Aguardando o numero de entradas...\n");
    bzero(buf,N_BUF);
    n = recvfrom(sock,buf,N_BUF,0,(struct sockaddr *)&from,&fromlen);
    
    int *n_inputs_ptr = (int *) buf;

    int n_inputs = converteASCIItoInt(n_inputs_ptr[0]);

    int16_t inputs[n_inputs][N];
    int16_t outputs[n_inputs][N];

    printf("Confirmando o recebimento de n_inputs:\n");
    n = sendto(sock,"1",1,0,(struct sockaddr *)&from,fromlen);
    if (n  < 0) printf("sendto");	

    for (int i = 0; i < n_inputs; i++) {
        printf("Aguardando as entradas...\n");
        bzero(buf,N_BUF);
        n = recvfrom(sock,buf,N_BUF,0,(struct sockaddr *)&from,&fromlen);

        split_str_to_ints16(buf, N, 4, inputs[i]);

        printf("Confirmando o recebimento:\n");
        n = sendto(sock,"1",1,0,(struct sockaddr *)&from,fromlen);
        if (n  < 0) printf("sendto");	
    }

    printf("Entradas recebidas");

    int current_input = 0;
    printf("Reset control bit\n");
    peripheral_write16(dualPortRam, 0, 0x0);
    printf("Writing numbers...\n");
    for (int i = 0; i < N; i++) {
        peripheral_write16(dualPortRam, NUMBERS_ADDR_BASE + i, inputs[current_input][i]);
    }
    current_input++;
    printf("Set control bit\n");
    peripheral_write16(dualPortRam, CONTROL_ADDR, 0x1);
    

    int current_output = 0;
	while(1)
	{
		if (peripheral_read16(dualPortRam,STAGE2_STATUS_ADDR)) {
            for (int i = 0; i < N; i++) {
                outputs[current_output][i] = peripheral_read16(dualPortRam, RESULT_ADDR_BASE + i);
                //printf("Endereco: %X, Valor: %X\n", 4*i, outputs[current_output][i]);
		    }
            current_output++;
        }

        if (peripheral_read16(dualPortRam,STAGE1_STATUS_ADDR) && current_input < n_inputs) {
            printf("Reset control bit\n");
            peripheral_write16(dualPortRam, 0, 0x0);
            printf("Writing numbers...\n");
            for (int i = 0; i < N; i++) {
                peripheral_write16(dualPortRam, NUMBERS_ADDR_BASE + i, inputs[current_input][i]);
            }
            printf("Set control bit\n");
            peripheral_write16(dualPortRam, CONTROL_ADDR, 0x1);
            current_input++;
        }

        if (current_output == n_inputs) break;
	}	

    for (int i = 0; i < n_inputs; i++) {
        char result_buf[N_BUF];
        ints16_to_str_fixed_width(outputs[i], N, 4, result_buf);

        if (n < 0) printf("recvfrom");
        else
        {
            printf("Esperando um tempo\n");
            usleep(1000); //Esperando um tempo para ver se o python espera a mensagem;
            printf("Devolvendo pacote recebido:\n");
            n = sendto(sock,result_buf,N_BUF,0,(struct sockaddr *)&from,fromlen);
            if (n  < 0) printf("sendto");						
        }
    }

    
    

    
}