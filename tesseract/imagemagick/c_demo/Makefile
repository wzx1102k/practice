APP_SRCS	= ${wildcard *.c}

APP_OBJS = $(APP_SRCS:.c=.o)

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
#Include += -I `Magick++-config --cppflags --cxxflags --ldflags --libs`
#LIB_PATH += -L /usr/local/lib
Include += `pkg-config --cflags --libs MagickCore`
MAKEFILE = Makefile

CC = cc

all: demo_imagemagick convert.so

$(APP_OBJS): %.o: %.c
	$(CC) -c -fPIC $(Include) $*.c

demo_imagemagick: $(OBJS)
	$(CC) -o $@ $(OBJS) $(Include)
#$(APP_OBJS): %.o: %.c
#	$(CC) -c $(Include) $*.c

convert.so: $(OBJS)
	$(CC) -shared -fPIC -o $@ $(OBJS) $(Include)
#$(APP_OBJS): %.o: %.c
#	$(CC) -c -fPIC $(Include) $*.c

clean:
	rm -f $(OBJS) demo_imagemagick convert.so
rebuild:
	make clean
	make
