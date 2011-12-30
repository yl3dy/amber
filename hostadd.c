#include "hostadd.h"

void amber_host_add()
{
	std::string custom_hostname, ip_addr;
	std::cin >> custom_hostname >> ip_addr;

	// check'em
	std::string hostname_expr = "[a-zA-Z0-9]";
	std::string ip_addr_expr = "\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b";
	boost::regex chk_host(hostname_expr);
	boost::regex chk_ip_addr(ip_addr_expr);

	if(boost::regex_match(custom_hostname, chk_host))
		std::cout << "Wrong hostname\n";
	if(boost::regex_match(ip_addr, chk_ip_addr))
		std::cout << "Wrong ip\n";
    amber_db_init_all();
	amber_db_insert_host_union(custom_hostname.c_str(), ip_addr.c_str());
}
