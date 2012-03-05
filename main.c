#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <boost/filesystem.hpp>

using std::cout; using std::cerr;

#include "init.hpp"
#include "hostadd.h"
#include "update-host.h"
void print_usage();

//const char lockfile_path[] = "/var/lock/amber.lock";
const char lockfile_path[] = "/tmp/amber.lock";
bool lock_search();
bool is_locked();
void unlock_search();

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
       if(!is_locked())
	   {
           // do some search
           cout << "Searching\n";
	   }
    }
    else if(strcmp(argv[1],"update-all")==0)
    {
        lock_search();
        // do update-all
        unlock_search();
    }
    else if(strcmp(argv[1],"update-host")==0)
    {
        lock_search();
        update_host();
		unlock_search();
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

bool lock_search()
{
    std::ofstream lockfile(lockfile_path);
    if(!lockfile)
    {
        cerr << "Couldn't create lockfile. Aborting.\n";
        return false;
    }
    lockfile << " ";    // just to be sure that the file will be actually created
    return true;
}
void unlock_search()
{
    using namespace boost::filesystem;

    path lk(lockfile_path);
    if(!remove(lk))
        cerr << "Couldn't remove lockfile. You have been warned.\n";
}
bool is_locked()
{
    using namespace boost::filesystem;

    path lk(lockfile_path);
    return exists(lk);
}
