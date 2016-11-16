APP_SRCS	= ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)
OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
Include += `pkg-config --cflags opencv` -I .
LIBS += `pkg-config --libs opencv`
MAKEFILE = Makefile

CC = g++

all: server

server: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LIBS)
$(APP_OBJS): %.o: %.cpp
	$(CC) -c -fPIC  $*.cpp $(Include)
clean:
	rm -f $(OBJS) server
rebuild:
	make clean
	make
