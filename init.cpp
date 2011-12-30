#include "init.hpp"
#include <iostream>
#include <stdlib>
#include <stdlio>
//mysql_query("DROP DATABASE IF EXISTS Inform") or die("Could not delete db:". mysql_error());
//mysql_query("CREATE DATABASE Inform") or die("Could not delete db:". mysql_error());
//mysql_select_db('korvin') or die("Could not select_db :". mysql_error());
//mysql_query("DROP TABLE IF EXISTS   KIRI;") or die("Could not delete :". mysql_error());
void init()
{
    if(mysql_query("DROP DATABASE IF EXISTS AINDEX")!=0)
    
}
