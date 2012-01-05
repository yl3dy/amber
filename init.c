#include "init.h"
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <mysql/my_global.h>
#include <mysql/my_sys.h>
#include "db-backend.h"

void init()
{
    amber_db_init_all();
    char buf[1024];
    //sprintf(buf,"DROP DATABASE IF EXISTS %s",amber_db_getname());
    //amber_db_query(buf);
    //sprintf(buf,"CREATE DATABASE %s",amber_db_getname());
    //amber_db_query(buf);
    amber_db_enter();
    sprintf(buf,"DROP TABLE IF EXISTS HOST_UNION");
    amber_db_query(buf);
    sprintf(buf,"DROP TABLE IF EXISTS FULLINDEX");
    amber_db_query(buf);
    sprintf(buf,"DROP TABLE IF EXISTS TEMPINDEX");
    amber_db_query(buf);
    sprintf(buf,"CREATE TABLE HOST_UNION (name VARCHAR (256)  NOT NULL,ip_addr VARCHAR (20)  NOT NULL,PRIMARY KEY (ip_addr))");
    amber_db_query(buf);
    sprintf(buf,"CREATE TABLE FULLINDEX (host VARCHAR (256)  NOT NULL,path VARCHAR (1024)  NOT NULL,name VARCHAR (1024)  NOT NULL, link VARCHAR (1000)  NOT NULL,size INT(11))");
    amber_db_query(buf);
    sprintf(buf,"CREATE TABLE TEMPINDEX (host VARCHAR (256)  NOT NULL,path VARCHAR (1024)  NOT NULL,name VARCHAR (1024)  NOT NULL, link VARCHAR (1000)  NOT NULL,size INT(11))");
    amber_db_query(buf);
}
