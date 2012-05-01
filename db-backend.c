#include "db-backend.h"
const char db_name[]="AINDEX";
MYSQL mysql;
void amber_db_init_all()
{
    mysql_init(&mysql);
    mysql_real_connect(&mysql,"localhost","root","windfree7",NULL,0,NULL,0);
}
void amber_db_close()
{
    mysql_close(&mysql);
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

Result * amber_db_search(char * str,long long * num)
{
    //SELECT name,host,link  from FULLINDEX where (locate('linux',name)>0);
    MYSQL_RES *result;
    unsigned int num_fields;
    unsigned int num_rows;
    Result * Out;
    if (mysql_query(&mysql,str))
    {
	// ошибка
    }
    else // запрос выполнен, обработка возвращенных им данных
    {
        result = mysql_store_result(&mysql);
        if (result) // содержит строки
        {
            num_fields = mysql_num_fields(result);
            long long  all_ou=mysql_num_rows(result);
            *num=all_ou;
            MYSQL_ROW row;
            Out=new Result[all_ou];
            int i=0;
            while ((row = mysql_fetch_row(result)))
            {
                unsigned long *lengths;
                lengths = mysql_fetch_lengths(result);
                strcpy(Out[i].Name,row[0]);
                strcpy(Out[i].Host,row[1]);
                strcpy(Out[i].link,row[2]);
                i=i+1;
               // printf(Out[i].link);
                
               // for(i = 0; i < num_fields; i++)
               // {
              //      printf("[%.*s] ", (int) lengths[i], row[i] ? row[i] : "NULL");
              //  }
               // printf("\n");
            
            }
            // извлечение строк, затем вызов mysql_free_result(result
            mysql_free_result(result);
        }
        else // mysql_store_result() не вернула ничего; может ли что-либо вернуть?
        {
            if(mysql_field_count(&mysql) == 0)
            {
                // запрос не возвращает данные
                // (запрос не был вида SELECT)
                fprintf(stderr, "wtf?????????????????????\n");
            }
            else // mysql_store_result() должна была вернуть данные
            {
                fprintf(stderr, "Error: %s\n", mysql_error(&mysql));
            }
        }
    }
    return Out;
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
    
    char buf[3024];
    snprintf(buf,3024,"INSERT INTO FULLINDEX (host,path,name,link,size) VALUES('%s','%s','%s','smb://%s%s/%s','%i');",th,tp,tn,th,tp,tn,size);
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
