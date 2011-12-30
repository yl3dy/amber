#include "init.hpp"
//mysql_query("DROP DATABASE IF EXISTS Inform") or die("Could not delete db:". mysql_error());
//mysql_query("CREATE DATABASE Inform") or die("Could not delete db:". mysql_error());
//mysql_select_db('korvin') or die("Could not select_db :". mysql_error());
//mysql_query("DROP TABLE IF EXISTS   KIRI;") or die("Could not delete :". mysql_error());
void init()
{
    mysql_query("DROP DATABASE IF EXISTS ");// die("Could not delete db:". mysql_error());      
}
