#ifndef DB_BACKEND_H_INCLUDED
#define DB_BACKEND_H_INCLUDED

#include <string>
#include <mysql/my_global.h>
#include <mysql/my_sys.h>
#include <mysql.h>
#include <mysql/mysql_com.h>


void amber_init_all();    //connect to db
void amber_enter();       //select db 
void amber_query(char *); //for mysql_query
void amber_db_host_add(std::string custom_hostname,std::string  ip_addr);

#endif // DB_BACKEND_H_INCLUDED
