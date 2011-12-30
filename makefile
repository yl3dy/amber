SOURCES=main.c init.c hostdel.c db-backend.c search.c update-all.c update-host.c hostadd.c

OBJDIR=obj
OBJECTS=$(addprefix $(OBJDIR)/,$(SOURCES:.c=.o))
EXECUTABLE=oberon

CC=g++
CCFLAGS=-Wall -x c++ -g -I/usr/include/mysql -DUSE_OLD_FUNCTIONS
LDFLAGS=-lmysqlclient

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CCFLAGS) $(LDFLAGS) -o $@ $^

$(OBJDIR)/%.o: %.c $(HEADERS)
	ls obj > /dev/null 2>&1 || mkdir obj
	$(CC) $(CCFLAGS) -c -o $@ $<

clean:
	rm -f obj/* $(EXECUTABLE)
