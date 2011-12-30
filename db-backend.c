#include "db-backend.h"

const char db_name[]="AINDEX";
MYSQL mysql;
void amber_db_init_all()
{
    mysql_init(&mysql);
    mysql_real_connect(&mysql,"localhost","root","windfree7",NULL,0,NULL,0);
    
}
void amber_db_enter()
{
    
}
void amber_db_query(char * str)
{
    
}
void amber_db_host_add(std::string custom_hostname,std::string  ip_addr)
{
    
}
