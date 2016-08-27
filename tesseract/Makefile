APP_SRCS = ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OCR_JAVA_OBJS = ocr_java.o ocr_tesseract.o

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)

Include += -I /usr/lib/jvm/java-7-openjdk-amd64/include
LIBS += -locr_tesseract
LIB_PATH += -L .
MAKEFILE = Makefile

CC = g++
AR = ar rs

all: ocr_demo libocr_java.a
ocr_demo: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LIBS) $(LIB_PATH) -static
$(APP_OBJS): %.o: %.cpp
	$(CC) -c -static $(Include) $*.cpp

libocr_java.a: $(OCR_JAVA_OBJS)
	$(AR) $@ $(OCR_JAVA_OBJS)

clean:
	rm -f $(OBJS) ocr_demo libocr_java.a
lib: libocr_java.a
rebuild:
	make clean
	make
