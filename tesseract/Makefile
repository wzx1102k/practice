APP_SRCS = ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OCR_JAVA_OBJS = ocr_java.o ocr_tesseract.o

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)

Include += -I /usr/lib/jvm/java-7-openjdk-amd64/include
STATIC_LIBS += -locr_tesseract
LIBS +=
LIB_PATH += -L .
MAKEFILE = Makefile

CC = g++
AR = ar rs

all: ocr_demo libocr_java.a libocr_java.so
ocr_demo: $(OBJS)
	$(CC) -o $@ $(OBJS) $(STATIC_LIBS) $(LIB_PATH) -static
$(APP_OBJS): %.o: %.cpp
	$(CC) -fPIC -c $(Include) $*.cpp

libocr_java.a: $(OCR_JAVA_OBJS)
	$(AR) $@ $(OCR_JAVA_OBJS)

libocr_java.so: $(OCR_JAVA_OBJS)
	$(CC) -fPIC -shared -o $@ $(OCR_JAVA_OBJS) $(LIBS) $(LIB_PATH)
clean:
	rm -f $(OBJS) ocr_demo libocr_java.a

static_lib: libocr_java.a
shared_lib: libocr_java.so
rebuild:
	make clean
	make
