APP_SRCS = ${wildcard *.c}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
MAKEFILE = Makefile

CC = gcc

all: server client

server:
	$(CC) -c server.c
	$(CC) -o $@ server.o

client:
	$(CC) -c client.c
	$(CC) -o $@ client.o

clean:
	rm -f server client *.o
rebuild:
	make clean
	make
