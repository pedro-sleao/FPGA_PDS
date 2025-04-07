/*
* FUNCAO : Primeiro codigo para apenas imprimir Ola mundo no console do linux embarcado
* PROJETO: Notas de aula da Tópicos e Comunicações 2
* DATA DE CRIACAO: 25/03/2025
*/


//Para o codigo basico de comunicacao FPGA-HPS
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include "hwlib.h"
#include "socal.h"
#include "hps.h"
#include "alt_gpio.h"
#include "hps_0.h"

//Para o codigo basico de comunicao SoC-Computador
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



int main() 
{

	printf("*---------------------------------------------------------------------\n");
	printf("* FUNCTION       : Primeiro Projeto no HPS\n");
	printf("* PROJECT        : Tópicos em Comunicações 2 - 2025.1\n");
	printf("* DATE           : 25/03/2025\n");
	printf("*---------------------------------------------------------------------\n");

	usleep(10000); //para as threads pelo tempo passado no argumento em microsegundos 
	
	return(0);
}
