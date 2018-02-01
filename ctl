#!/bin/bash

start()
{
    pid=$(pgrep -f "supervisord")
    if [ "x$pid" == "x" ]; then
        supervisord -c app.conf
    else
        supervisorctl -c app.conf start all
    fi
}

stop()
{
    pid=$(pgrep -f "supervisord")
    if [ "x$pid" != "x" ]; then
        supervisorctl -c app.conf shutdown
        sleep 3
    fi
}

case $1 in
    start)
        echo 'start'
        start
        ;;
    stop)
        echo 'stop'
        stop
        ;;
    restart)
        echo 'restart ...'
        stop
        start
        ;;
    status)
        supervisorctl -c app.conf status
        ;;
esac
