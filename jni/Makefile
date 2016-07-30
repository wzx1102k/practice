APP_SRCS	= ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
LIBS += -lpthread 
Include += -I /tools/jdk1.6.0_38/include
Include += -I /tools/jdk1.6.0_38/include/linux

MAKEFILE = Makefile

CC = g++

all: libhello.so

libhello.so: $(OBJS)
	$(CC) -shared -fPIC -o $@ $(OBJS) $(LIBS)
$(APP_OBJS): %.o: %.cpp
	$(CC) -c -fPIC $(Include) $*.cpp

clean:
	rm -f $(OBJS) libhello.so
rebuild:
	make clean
	make
