#include "update-host.h"
void update_host_work(char *ip)
{
    system("mkdir -p /tmp/some_for_smb");
    char command[1024];
    snprintf(command,1024,"smbmount -o guest //%s/ /tmp/some_for_smb",ip);
    //!!What to do with ///93.175.4.4./pub 
    //!!The function knows only ip - we need to solve it
    system(command);
    
    snprintf(command,1024,"cd /tmp/some_for_smb");
    system(command);
    FILE *fp = popen("find -type f", "r+" );
    char buff[1024];
    while(!fgets( buff,1024, fp))//this isn't work . I will do it later,when i return
    {
        printf("%s\n",buff);
    }
		
    snprintf(command,1024,"umount /tmp/some_for_smb");
    system(command);
    
}
void update_host()
{
    char ip[80];
    std::cin>>ip;
    //!!ADD CHECKING HERE!!!!
    update_host_work(ip);
}
