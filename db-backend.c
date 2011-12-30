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
    mysql_select_db(&mysql,db_name);
}
void amber_db_query(char * str)
{
    mysql_query(&mysql,str);
}
void amber_db_insert_host_union(const char * hostname,const char * ip_addr)
{
    
}
const char * amber_db_getname()
{
    return db_name;
}
