APP_SRCS = ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OCR_JAVA_OBJS = ocr_java.o ocr_tesseract.o

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)

INCLUDE += -I /usr/lib/jvm/java-7-openjdk-amd64/include
STATIC_LIBS = -locr_tesseract
STATIC_LIB_PATH += -L .
LIBS += -ltesseract -llept -ljpeg -ltiff -lpng -ljbig
LIB_PATH += -L . -L ./share_lib
INCLUDE += -I ./include
MAKEFILE = Makefile

CC = g++
AR = ar rs

all: libocr_java.a libocr_java.so ocr_share_demo ocr_static_demo
$(APP_OBJS): %.o: %.cpp
	$(CC) -fPIC -c $(INCLUDE) $*.cpp

libocr_java.a: $(OCR_JAVA_OBJS)
	$(AR) $@ $(OCR_JAVA_OBJS)

libocr_java.so: $(OCR_JAVA_OBJS)
	$(CC) -fPIC -shared -o $@ $(OCR_JAVA_OBJS) $(LIBS) $(LIB_PATH) $(INCLUDE)

ocr_share_demo: $(OBJS)
	$(CC) -fPIC -o $@ $(OBJS) -locr_java $(LIBS) $(LIB_PATH) $(INCLUDE) 

ocr_static_demo: $(OBJS)
	$(CC) -o $@ $(OBJS) $(STATIC_LIBS) $(STATIC_LIB_PATH) $(INCLUDE) -static

clean:
	rm -f $(OBJS) ocr_static_demo libocr_java.a libocr_java.so ocr_share_demo

static_lib: libocr_java.a
shared_lib: libocr_java.so
rebuild:
	make clean
	make
