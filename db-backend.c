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
    char buf[1024];
    snprintf(buf,1024,"INSERT INTO HOST_UNION (name,ip_addr) VALUES('%s','%s');",hostname,ip_addr);
    amber_db_query(buf);
    std::cout<<mysql_error(&mysql);
}
void amber_db_insert_fullindex(const char * hostname,const char * path,const char * name,int size)
{
    char buf[1024];
    snprintf(buf,1024,"INSERT INTO FULLINDEX (host,path,name,link,size) VALUES('%s','%s','%s','smb://%s/%s/%s','%i');",
                                                                               hostname,path,name,hostname,path,name,size);
    amber_db_query(buf);
}
void amber_db_standart_init()
{
    amber_db_init_all();
    amber_db_enter();
}
const char * amber_db_getname()
{
    return db_name;
}
