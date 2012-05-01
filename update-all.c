#include "update-all.h"
void update_all()
{
 amber_db_standart_init();
 char buf[1025];
 sprintf(buf,"SELECT * FROM HOST_UNION");
 amber_db_query(buf);
    
}
