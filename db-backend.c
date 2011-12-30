#include "db-backend.h"

const char db_name[]="AINDEX";
MYSQL mysql;
void amber_init_all()
{
    mysql_init(&mysql);
    mysql_connect(&mysql,"localhost","root","windfree7");
    
}
void amber_enter()
{
    
}
void amber_query(char * str)
{
    
}
