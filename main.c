#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "init.hpp"
#include "hostadd.h"
void print_usage();

int main(int argc, char **argv)
{
    if(argc!=2)
    {
        print_usage();
        return 1;
    }
    if(strcmp(argv[1],"init")==0)
    {
        init();
    }
    else if(strcmp(argv[1],"hostadd")==0)
    {
        amber_host_add();
    }
    else if(strcmp(argv[1],"hostdel")==0)
    {
        
    }
    else if(strcmp(argv[1],"search")==0)
    {
        
    }
    else if(strcmp(argv[1],"update-all")==0)
    {
        
    }
    else if(strcmp(argv[1],"update-host")==0)
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
