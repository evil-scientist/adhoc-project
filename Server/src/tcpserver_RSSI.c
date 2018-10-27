/*
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>    
#include <sys/socket.h>
#include <arpa/inet.h> 
#include <unistd.h>   
#include "AdhocServer.h"
#include "CommandList.h"


//#define __DEBUG__ 1

unsigned int con_count = 0;

int main(int argc , char *argv[])
{
    int socket_desc , c , read_size;
    struct sockaddr_in server , client;
    int cmd_val= 0; 
    int val;
    int  ret = 0;
    int i = 0;
    if (argc != 2) {
        printf("Please enter %s  <NUMBER OF BOTS>\n",argv[0]);
        exit(0);
    }
    NUM_CONNECTIONS = atoi(argv[1]);

    BOT_ID = (char *)malloc(NUM_CONNECTIONS * sizeof(char));
    memset(BOT_ID,0,NUM_CONNECTIONS);
    client_sock = (int *)malloc(NUM_CONNECTIONS * sizeof(int));
    memset(BOT_ID,0,NUM_CONNECTIONS * sizeof(int));

    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }
    puts("\n");
    puts("******* Server control program (Adhoc networking course) *******");
    puts("\n");

    puts("* Socket created");

    int option = 1;
    setsockopt(socket_desc, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(TCP_PORT);

    //Bind
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        //print the error message
        perror("bind failed. Error");
        return 1;
    }
    puts("* Binding done");


    //Listen
    listen(socket_desc , 3);

    //Accept and incoming connection

    while(con_count != NUM_CONNECTIONS) {

        c = sizeof(struct sockaddr_in);
        puts("* Waiting for bots to connect");

        //accept connection from an incoming client
        client_sock[con_count] = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
        if (client_sock[con_count] < 0)
        {
            perror("accept failed");
            return 1;
        }
        printf("  - Accepted connection\n");
#ifdef __DEBUG__
        printf("Got new  sockfd %d\n",client_sock[con_count]);
#endif
        BOT_ID[con_count] = get_botID(con_count);
        printf("  - Bot with ID : <%d> Connected\n",BOT_ID[con_count]);
        con_count++;
    }
    printf("-----------------------------------------------------------\n");


    /* EDITED PART ========================================================= */
    int repeats = 0;

    int dist = 0;
    FILE *fout = fopen("log.txt", "w");
    printf("Enter the damn number of repetitions, you fool");
    scanf("%d", &repeats);	
    printf("Team SURYA super power action start!\n\n");
    dst_id = 2;	
    while(1) {
		

        printf("Gimme the distance, u damn fuk: ");
        scanf("%d", &dist);

	if (dist == -1){
		fclose(fout);
 		return 0;
	}

        printf("What a shitty distance, ewgh :(\n");
        fprintf(fout, "Measuring at distance: %d\n", dist);

        for (int i=0; i<repeats; i++) {

            long rssi = get_RSSI(src_id, dst_id);
            printf("%ld\n", rssi);
            fprintf(fout, "%ld\t", rssi);

        }

        printf("\n");
        fprintf(fout, "\n");
	
        //return 0;
    }
}

