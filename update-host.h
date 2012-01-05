#ifndef UPDATE_HOST_H_INCLUDED
#define UPDATE_HOST_H_INCLUDED
#include <iostream>
#include <string.h>
#include <cstdlib>
#include <cstdio>
#include <libgen.h>
#include <vector>
#include <sys/stat.h>
#include "db-backend.h"
void update_host_work(char *ip);
void update_host();
#endif // UPDATE_HOST_H_INCLUDED
