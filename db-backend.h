#ifndef DB_BACKEND_H_INCLUDED
#define DB_BACKEND_H_INCLUDED

#include <string>
#include <cstring>
#include <iostream>
#include <mysql/my_global.h>
#include <mysql/my_sys.h>
#include <mysql.h>
#include <mysql/mysql_com.h>
struct Result
{
    char Host[256];
    char Name[1024];
    char link[1024];
    int size;
};

void amber_db_init_all();    //connect to db
void amber_db_enter();       //select db 
void amber_db_standart_init(); // connect and select
void amber_db_query(char *); //for mysql_query
void amber_db_insert_host_union(const char * hostname,const char * ip_addr);
void amber_db_insert_fullindex(const char * hostname,const char * path,const char * name,int size);
Result * amber_db_search(char * str,long long * num);
const char * amber_db_getname();

#endif // DB_BACKEND_H_INCLUDED
