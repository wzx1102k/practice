APP_SRCS	= ${wildcard *.c}
#APP_SRCS = convert.c

APP_OBJS = $(APP_SRCS:.c=.o)
#APP_OBJS = demo_conv.o
CONV_OBJS = convert.o

#OBJS = $(APP_OBJS)
OBJS = demo_conv.o
SRCS = $(APP_SRCS)
#Include += -I `Magick++-config --cppflags --cxxflags --ldflags --libs`
#LIB_PATH += -L /usr/local/lib
Include += `pkg-config --cflags --libs MagickCore`
MAKEFILE = Makefile
LIBS = -lconvert
LIB_PATH += -L .
#CC = cc
CC = gcc
AR = ar r
all: demo_conv libconvert.so libconvert.a

$(APP_OBJS): %.o: %.c
	$(CC) -c -fPIC $(Include) $*.c

demo_conv: $(OBJS) libconvert.so
	$(CC) -o $@ $(OBJS) $(LIBS) $(LIB_PATH)
#$(APP_OBJS): %.o: %.c
#	$(CC) -c $(Include) $*.c

libconvert.so: $(CONV_OBJS)
	$(CC) -shared -fPIC -o $@ $(CONV_OBJS) $(Include)
#$(APP_OBJS): %.o: %.c
#	$(CC) -c -fPIC $(Include) $*.c

libconvert.a: $(CONV_OBJS)
	$(AR) $@ $(CONV_OBJS)
clean:
	rm -f $(APP_OBJS) demo_conv libconvert.so libconvert.a
rebuild:
	make clean
	make
