APP_SRCS	= ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
LIBS += -llept -ltesseract
Include += -I /usr/local/include
Include += -I /usr/local/include/leptonica
Include += -I ./imagemagick/c_demo
Include += `pkg-config --cflags --libs MagickCore`
LIBS += -lconvert
LIB_PATH += -L /usr/local/lib
LIB_PATH += -L ./imagemagick/c_demo
MAKEFILE = Makefile

CC = g++

all: demo_tesseract

demo_tesseract: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LIB_PATH) $(LIBS)
$(APP_OBJS): %.o: %.cpp
	$(CC) -c -fPIC $(Include) $*.cpp

clean:
	rm -f $(OBJS) demo_tesseract
rebuild:
	make clean
	make
