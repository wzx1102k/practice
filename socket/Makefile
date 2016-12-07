APP_SRCS	= ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)
OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
Include += -I .
LIBS = 
#Include += `pkg-config --cflags opencv` -I .
#LIBS += `pkg-config --libs opencv`
MAKEFILE = Makefile
CFLAGS = -pg -W -g -fPIC
CC = g++

all: server

server: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LIBS)
$(APP_OBJS): %.o: %.cpp
	$(CC) $(CFLAGS) -c $*.cpp $(Include)
clean:
	rm -f $(OBJS) server
rebuild:
	make clean
	make
