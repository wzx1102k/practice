APP_SRCS = ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
Include += -I /usr/local/include
Include += -I /usr/local/include/leptonica
Include += -I ./imagemagick/c_demo
Include += -I /usr/include
Include += -I /home/cloud/cloud-git-master/practice/tesseract/jbig/jbigkit-2.1/libjbig
#Include += `pkg-config --cflags --libs MagickCore`
LIBS += -ltesseract -llept -ltiff -lpng -ljpeg -ljbig -llzma -lpthread -lz -lm
LIB_PATH += -L /usr/local/lib
LIB_PATH += -L /usr/lib/x86_64-linux-gnu
LIB_PATH += -L ./imagemagick/c_demo
LIB_PATH += -L /home/cloud/cloud-git-master/practice/tesseract/jbig/jbigkit-2.1/libjbig
MAKEFILE = Makefile

CC = g++

all: demo_tesseract

demo_tesseract: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LIBS) $(LIB_PATH) -static
$(APP_OBJS): %.o: %.cpp
	$(CC) -c -static $(Include) $*.cpp

clean:
	rm -f $(OBJS) demo_tesseract
rebuild:
	make clean
	make
