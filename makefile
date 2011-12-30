SOURCES=main.cpp init.cpp

OBJDIR=obj
OBJECTS=$(addprefix $(OBJDIR)/,$(SOURCES:.cpp=.o))
EXECUTABLE=oberon

CC=g++
CCFLAGS=-Wall -g -I/usr/include/mysql
LDFLAGS=-lmysqlclient

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CCFLAGS) $(LDFLAGS) -o $@ $^

$(OBJDIR)/%.o: %.cpp $(HEADERS)
	ls obj > /dev/null 2>&1 || mkdir obj
	$(CC) $(CCFLAGS) -c -o $@ $<

clean:
	rm -f obj/* $(EXECUTABLE)
