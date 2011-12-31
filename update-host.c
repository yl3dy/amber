#include "update-host.h"
void update_host_work(char *ip)
{
    system("mkdir -p /tmp/some_for_smb");
    char command[1024];
    snprintf(command,1024,"smbmount -o guest //%s/ /tmp/some_for_smb",ip);
    //!!What to do with //93.175.4.4./pub 
    //!!The function knows only ip - we need to solve it
    //!!For testing enter "93.175.4.4./pub" 
    system(command);
    FILE *fp = popen("cd /tmp/some_for_smb && find -type f", "r" );
    char buff[1024];
    if(fp==NULL) 
        printf("ewf\n");//,buff);
    amber_db_standart_init();
    fgets( buff,1024, fp);
    while(!feof(fp))
    {
        std::string tmp(buff);
        tmp=tmp.substr(1,tmp.length()-2);
        char file_nm[1024],dirn[1024],tmpo[1024];
        strcpy(tmpo,tmp.c_str());
        strcpy(file_nm,basename(tmpo));
        strcpy(dirn,dirname(tmpo));
        
        struct stat sb;
        tmp=std::string("/tmp/some_for_smb")+tmp;
        stat(tmp.c_str(),&sb);
        
        amber_db_insert_fullindex(ip,dirn,file_nm,(long long)sb.st_size);
        fgets( buff,1024, fp); 
    }
		
    snprintf(command,1024,"umount /tmp/some_for_smb/");
    system(command);
    
}
void update_host()
{
    char ip[80];
    std::cin>>ip;
    //!!ADD CHECKING HERE!!!!
    update_host_work(ip);
}
