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
    std::cout<<mysql_error(&mysql);
}
void amber_db_query(char * str)
{
    if(mysql_query(&mysql,str)!=0)
        std::cout<<mysql_error(&mysql)<<std::endl;
}
void amber_db_insert_host_union(const char * hostname,const char * ip_addr)
{
    char buf[1024];
    
    char th[3048];
    mysql_real_escape_string(&mysql, th,hostname,strlen(hostname));
    char tp[3048];
    mysql_real_escape_string(&mysql, tp,ip_addr,strlen(ip_addr));
    snprintf(buf,1024,"INSERT INTO HOST_UNION (name,ip_addr) VALUES('%s','%s');",th,tp);
    amber_db_query(buf);
}
void amber_db_insert_fullindex(const char * hostname,const char * path,const char * name,int size)
{
    
    char th[3048];
    mysql_real_escape_string(&mysql, th,hostname,strlen(hostname));
    char tp[3048];
    mysql_real_escape_string(&mysql, tp,path,strlen(path));
    char tn[3048];
    mysql_real_escape_string(&mysql, tn,name,strlen(name));
    
    char buf[1024];
    snprintf(buf,1024,"INSERT INTO FULLINDEX (host,path,name,link,size) VALUES('%s','%s','%s','smb://%s%s/%s','%i');",th,tp,tn,th,tp,tn,size);
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
