#include "update-host.h"
void work_with_shara(const char *ip,const char *fold)
{
    system("mkdir -p /tmp/some_for_smb");
    char command[1024];
    char buff[1024];
    snprintf(command,1024,"smbmount -o guest //%s/%s/ /tmp/some_for_smb",ip,fold);
    system(command);
    FILE *fp = popen("cd /tmp/some_for_smb && find -type f", "r" );
    
    if(fp==NULL) 
        printf("WTF? \n");//,buff);
    fgets( buff,1024, fp);
    while(!feof(fp))
    {
        std::string tmp(buff);
        tmp=tmp.substr(1,tmp.length()-2);
        char file_nm[1024],dirn[1024],tdirn[1024],tmpo[1024];
        strcpy(tmpo,tmp.c_str());
        strcpy(file_nm,basename(tmpo));
        strcpy(tdirn,dirname(tmpo));
        sprintf(dirn,"/%s%s",fold,tdirn);
        struct stat sb;
        tmp=std::string("/tmp/some_for_smb")+tmp;
        stat(tmp.c_str(),&sb);
        
        amber_db_insert_fullindex(ip,dirn,file_nm,(long long)sb.st_size);
        fgets( buff,1024, fp); 
    }
		
    fclose(fp);
    snprintf(command,1024,"umount /tmp/some_for_smb/");
    system(command);
}
void update_host_work(char *ip)
{
    char command[1024];
    char buff[1024];
    sprintf(command,"smbclient -L //%s/ -N |awk 'BEGIN{FS=\" \"} {if(NR>3){if($2==\"Disk\"){print $1}}}' ",ip);
    FILE *awkp=popen(command, "r");
    std::vector<std::string> shars;
    fgets(buff,1024, awkp);
    while(!feof(awkp))
    {
        std::string nsh(buff);
        shars.push_back(nsh.substr(0,nsh.length()-1));
        fgets(buff,1024, awkp);
    }
    fclose(awkp);
    for(int i=0;i<shars.size();i++)
        work_with_shara(ip,shars[i].c_str());
        //std::cout<<shars[i].c_str()<<std::endl;
}
void update_host()
{
    char ip[80];
    std::cin>>ip;
    //!!ADD CHECKING HERE!!!!
    
    amber_db_standart_init();
    update_host_work(ip);
    
}
