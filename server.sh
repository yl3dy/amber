#!/bin/bash

PIDFILE=/tmp/amber.pid
PORT=3033
HOST=127.0.0.1

case "$1" in
    "start")
        echo Starting fastcgi server
        python manage.py runfcgi method=prefork host=$HOST port=$PORT pidfile=$PIDFILE 
     ;;
     "stop")
        echo Stopping fastcgi server
        kill `cat $PIDFILE`
        rm $PIDFILE
        ;;
     "restart")
        $0 stop
        sleep 1
        $0 start
        ;;
    *) 
        echo "Usage: server.sh {start|stop|restart}"
        ;;
esac
