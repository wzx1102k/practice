APP_SRCS	= ${wildcard *.cpp}

APP_OBJS = $(APP_SRCS:.cpp=.o)

OBJS = $(APP_OBJS)
SRCS = $(APP_SRCS)
Include += -I `Magick++-config --cppflags --cxxflags --ldflags --libs`
#LIB_PATH += -L /usr/local/lib
MAKEFILE = Makefile

CC = c++

all: demo_imagemagick

demo_imagemagick: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LIB_PATH) $(LIBS)
$(APP_OBJS): %.o: %.cpp
	$(CC) -c $(Include) $*.cpp

clean:
	rm -f $(OBJS) demo_imagemagick
rebuild:
	make clean
	make
