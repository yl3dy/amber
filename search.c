#include "search.h"
#include <iostream>
void search()
{
    char Quest[512];
    std::cin.getline(Quest,511);
    amber_db_standart_init();
    long long res;
    char st[1024];
    sprintf(st,"SELECT name,host,link  from FULLINDEX where (locate('%s',name)>0);",Quest);
    Result * Our=amber_db_search(st,&res);
    std::cout<<res<<std::endl;
    for(int i=0;i<res;i++)
    {
        std::cout<<Our[i].link<<'\n';
    }
}
