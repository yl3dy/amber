SOURCES=main.c init.c hostdel.c db-backend.c search.c update-all.c update-host.c hostadd.c

OBJDIR=obj
OBJECTS=$(addprefix $(OBJDIR)/,$(SOURCES:.c=.o))
EXECUTABLE=oberon

CC=g++
CCFLAGS=-Wall -g -I/usr/include/mysql 
LDFLAGS=-lmysqlclient -lboost_regex -lboost_filesystem -lboost_system

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CCFLAGS) $(LDFLAGS) -o $@ $^

$(OBJDIR)/%.o: %.c $(HEADERS)
	ls obj > /dev/null 2>&1 || mkdir obj
	$(CC) $(CCFLAGS) -c -o $@ $<

clean:
	rm -f obj/* $(EXECUTABLE)
