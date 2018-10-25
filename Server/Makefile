EXEC=tcpserver
CFLAGS=
INC=-I header/ 
helloworld: tcp_command.o tcpserver.o
	gcc -o $(EXEC) -ggdb obj/tcpserver.o obj/tcp_command.o

tcp_command.o: src/tcp_command.c 
	gcc -c -ggdb src/tcp_command.c $(INC)
	mv *.o obj/
tcpserver.o: src/tcpserver.c 
	gcc -c -ggdb src/tcpserver.c $(INC) 
	mv *.o obj/

clean:
	rm obj/*.o ./tcpserver

