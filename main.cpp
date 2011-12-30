#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql/my_global.h>
#include <mysql/my_sys.h>
#include "init.hpp"
void print_usage();

int main(int argc, char **argv)
{
    MYSQL mysql;

    mysql_init(&mysql);
    //mysql_options(&mysql,MYSQL_READ_DEFAULT_GROUP,"your_prog_name");
    if (!mysql_connect(&mysql,"localhost","root","windfree7"))
    {
        fprintf(stderr, "Failed to connect to database: Error: %s\n",
          mysql_error(&mysql));
    }
    if(argc!=2)
    {
        print_usage();
        return 1;
    }
    my_init();
    if(strcmp(argv[1],"init")==0)
    {
        init();
    }
    else if(strcmp(argv[1],"hostadd")==0)
    {
        
    }
    else if(strcmp(argv[1],"hostdel")==0)
    {
        
    }
    else if(strcmp(argv[1],"search")==0)
    {
        
    }
    else if(strcmp(argv[1],"update")==0)
    {
        
    }
    else
    {
        print_usage();
        return 1;
    }
    return 0;
}

void print_usage()
{
    using std::cout;
    cout << "Bad arguments so GTFO.\n";
}
